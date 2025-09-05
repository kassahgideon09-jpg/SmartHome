#!/usr/bin/env python3
"""
AI Content Generator for TechReview Hub
Automatically generates product reviews and blog articles using OpenAI API
"""

import openai
import json
import os
import re
from datetime import datetime
from typing import Dict, List

class TechReviewAI:
    def __init__(self, api_key: str):
        """Initialize the AI content generator with OpenAI API key"""
        openai.api_key = api_key
        self.base_template_path = "."
        
    def generate_product_review(self, product_data: Dict) -> str:
        """Generate a complete product review HTML page"""
        
        prompt = f"""
        Create a comprehensive product review for {product_data['name']}.
        
        Product Details:
        - Name: {product_data['name']}
        - Category: {product_data['category']}
        - Price: ${product_data['price']}
        - Key Features: {', '.join(product_data['features'])}
        - Brand: {product_data['brand']}
        
        Write a detailed review including:
        1. Introduction paragraph
        2. Design and build quality section
        3. Performance and features section
        4. Pros and cons (6 pros, 5 cons)
        5. Final verdict with rating out of 5
        6. Value assessment
        
        Make it SEO-optimized, engaging, and include natural affiliate marketing elements.
        Write in a professional but approachable tone.
        Include specific technical details and real-world usage scenarios.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional tech reviewer with expertise in smart home devices and consumer electronics. Write detailed, honest, and helpful product reviews."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._create_review_html(product_data, content)
            
        except Exception as e:
            print(f"Error generating review: {e}")
            return None
    
    def generate_blog_article(self, topic: str, keywords: List[str]) -> str:
        """Generate a comprehensive blog article"""
        
        prompt = f"""
        Write a comprehensive blog article about "{topic}".
        
        Target Keywords: {', '.join(keywords)}
        
        Structure the article with:
        1. Engaging introduction (2-3 paragraphs)
        2. Table of contents
        3. 7-8 main sections with detailed content
        4. Product recommendations with affiliate potential
        5. Practical tips and actionable advice
        6. Conclusion with call-to-action
        
        Make it 2000+ words, SEO-optimized, and include natural product recommendations.
        Write for tech enthusiasts and smart home beginners.
        Include statistics, trends, and future predictions where relevant.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a tech industry expert and content creator specializing in smart home technology and consumer electronics trends."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._create_blog_html(topic, content, keywords)
            
        except Exception as e:
            print(f"Error generating article: {e}")
            return None
    
    def _create_review_html(self, product_data: Dict, ai_content: str) -> str:
        """Create complete HTML page for product review"""
        
        # Read the template
        try:
            with open('review-echo-dot.html', 'r', encoding='utf-8') as f:
                template = f.read()
        except FileNotFoundError:
            print("Template file not found. Make sure review-echo-dot.html exists.")
            return None
        
        # Extract sections from AI content
        sections = self._parse_ai_content(ai_content)
        
        # Generate filename
        filename = f"review-{product_data['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')}.html"
        
        # Replace template placeholders
        html_content = template
        
        # Update title and meta tags
        html_content = html_content.replace(
            "Amazon Echo Dot (5th Gen) Review - Smart Speaker Analysis | TechReview Hub",
            f"{product_data['name']} Review - {product_data['category']} Analysis | TechReview Hub"
        )
        
        html_content = html_content.replace(
            "Comprehensive review of the Amazon Echo Dot (5th Gen)",
            f"Comprehensive review of the {product_data['name']}"
        )
        
        # Update product name throughout
        html_content = html_content.replace("Amazon Echo Dot (5th Gen)", product_data['name'])
        html_content = html_content.replace("Echo Dot", product_data['name'])
        
        # Update price
        html_content = html_content.replace("$49.99", f"${product_data['price']}")
        
        # Update rating (generate based on pros/cons ratio)
        rating = self._calculate_rating(sections.get('pros', []), sections.get('cons', []))
        html_content = html_content.replace("4.8/5", f"{rating}/5")
        
        return html_content
    
    def _create_blog_html(self, topic: str, ai_content: str, keywords: List[str]) -> str:
        """Create complete HTML page for blog article"""
        
        try:
            with open('blog-smart-home-trends-2025.html', 'r', encoding='utf-8') as f:
                template = f.read()
        except FileNotFoundError:
            print("Template file not found. Make sure blog-smart-home-trends-2025.html exists.")
            return None
        
        # Generate filename
        filename = f"blog-{topic.lower().replace(' ', '-').replace('&', 'and')}.html"
        
        # Replace template content
        html_content = template
        
        # Update title and meta tags
        html_content = html_content.replace(
            "Top Smart Home Trends to Watch in 2025",
            topic
        )
        
        html_content = html_content.replace(
            "smart home trends 2025, home automation, AI technology, IoT devices, smart home future",
            ', '.join(keywords)
        )
        
        # Update date
        current_date = datetime.now().strftime("%B %d, %Y")
        html_content = html_content.replace("January 2, 2025", current_date)
        
        return html_content
    
    def _parse_ai_content(self, content: str) -> Dict:
        """Parse AI-generated content into structured sections"""
        sections = {}
        
        # Extract pros and cons
        pros_match = re.search(r'Pros:?\s*\n(.*?)(?=Cons:|$)', content, re.DOTALL | re.IGNORECASE)
        if pros_match:
            pros_text = pros_match.group(1)
            sections['pros'] = [line.strip('- ').strip() for line in pros_text.split('\n') if line.strip()]
        
        cons_match = re.search(r'Cons:?\s*\n(.*?)(?=\n\n|$)', content, re.DOTALL | re.IGNORECASE)
        if cons_match:
            cons_text = cons_match.group(1)
            sections['cons'] = [line.strip('- ').strip() for line in cons_text.split('\n') if line.strip()]
        
        return sections
    
    def _calculate_rating(self, pros: List[str], cons: List[str]) -> float:
        """Calculate product rating based on pros and cons"""
        if not pros and not cons:
            return 4.5
        
        pros_count = len(pros)
        cons_count = len(cons)
        
        # Base rating calculation
        if pros_count > cons_count * 2:
            return 4.8
        elif pros_count > cons_count:
            return 4.5
        elif pros_count == cons_count:
            return 4.2
        else:
            return 3.9
    
    def save_content(self, filename: str, content: str) -> bool:
        """Save generated content to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Content saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving content: {e}")
            return False

def main():
    """Main function to demonstrate AI content generation"""
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize AI generator
    ai = TechReviewAI(api_key)
    
    # Example product data
    sample_products = [
        {
            "name": "Google Nest Hub (2nd Gen)",
            "category": "Smart Display",
            "price": "99.99",
            "brand": "Google",
            "features": [
                "7-inch touchscreen display",
                "Google Assistant built-in",
                "Smart home control hub",
                "Sleep sensing technology",
                "Photo frame functionality"
            ]
        },
        {
            "name": "Ring Video Doorbell Pro 2",
            "category": "Smart Security",
            "price": "279.99",
            "brand": "Ring",
            "features": [
                "1536p HD video recording",
                "3D Motion Detection",
                "Two-way audio",
                "Advanced Pre-Roll technology",
                "Alexa integration"
            ]
        }
    ]
    
    # Example blog topics
    sample_topics = [
        "Best Smart Home Devices for Beginners in 2025",
        "How to Set Up a Complete Smart Home Security System",
        "Smart Speakers vs Smart Displays: Which Should You Choose?",
        "The Future of Home Automation: Trends to Watch"
    ]
    
    print("🤖 TechReview Hub AI Content Generator")
    print("=====================================")
    
    while True:
        print("\nOptions:")
        print("1. Generate Product Review")
        print("2. Generate Blog Article")
        print("3. Batch Generate Sample Content")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Generate single product review
            print("\nGenerating product review...")
            product = sample_products[0]  # Use first sample product
            review_html = ai.generate_product_review(product)
            
            if review_html:
                filename = f"review-{product['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')}.html"
                ai.save_content(filename, review_html)
                print(f"✅ Product review generated: {filename}")
            else:
                print("❌ Failed to generate product review")
        
        elif choice == '2':
            # Generate single blog article
            print("\nGenerating blog article...")
            topic = sample_topics[0]
            keywords = ["smart home", "home automation", "IoT devices", "tech review"]
            article_html = ai.generate_blog_article(topic, keywords)
            
            if article_html:
                filename = f"blog-{topic.lower().replace(' ', '-').replace(':', '').replace('?', '')}.html"
                ai.save_content(filename, article_html)
                print(f"✅ Blog article generated: {filename}")
            else:
                print("❌ Failed to generate blog article")
        
        elif choice == '3':
            # Batch generate sample content
            print("\nGenerating batch content...")
            
            # Generate reviews for all sample products
            for i, product in enumerate(sample_products):
                print(f"Generating review {i+1}/{len(sample_products)}: {product['name']}")
                review_html = ai.generate_product_review(product)
                
                if review_html:
                    filename = f"review-{product['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')}.html"
                    ai.save_content(filename, review_html)
                    print(f"✅ Generated: {filename}")
                else:
                    print(f"❌ Failed to generate review for {product['name']}")
            
            # Generate articles for sample topics
            for i, topic in enumerate(sample_topics[:2]):  # Generate first 2 topics
                print(f"Generating article {i+1}/2: {topic}")
                keywords = ["smart home", "automation", "tech guide", "2025 trends"]
                article_html = ai.generate_blog_article(topic, keywords)
                
                if article_html:
                    filename = f"blog-{topic.lower().replace(' ', '-').replace(':', '').replace('?', '')}.html"
                    ai.save_content(filename, article_html)
                    print(f"✅ Generated: {filename}")
                else:
                    print(f"❌ Failed to generate article: {topic}")
            
            print("\n🎉 Batch generation complete!")
        
        elif choice == '4':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()