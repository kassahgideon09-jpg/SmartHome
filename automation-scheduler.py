#!/usr/bin/env python3
"""
Automation Scheduler for TechReview Hub
Automatically schedules and runs AI content generation tasks
"""

import schedule
import time
import os
import json
import logging
from datetime import datetime, timedelta
from ai_content_generator import TechReviewAI

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

class AutomationScheduler:
    def __init__(self, api_key: str):
        """Initialize the automation scheduler"""
        self.ai = TechReviewAI(api_key)
        self.products_queue = []
        self.topics_queue = []
        self.load_content_queues()
        
    def load_content_queues(self):
        """Load content queues from JSON files"""
        try:
            # Load products queue
            if os.path.exists('products_queue.json'):
                with open('products_queue.json', 'r') as f:
                    self.products_queue = json.load(f)
            else:
                # Create default products queue
                self.products_queue = [
                    {
                        "name": "Apple HomePod Mini",
                        "category": "Smart Speaker",
                        "price": "99.99",
                        "brand": "Apple",
                        "features": [
                            "360-degree audio",
                            "Siri voice assistant",
                            "HomeKit integration",
                            "Intercom functionality",
                            "Compact design"
                        ]
                    },
                    {
                        "name": "Philips Hue Smart Bulb Starter Kit",
                        "category": "Smart Lighting",
                        "price": "199.99",
                        "brand": "Philips",
                        "features": [
                            "16 million colors",
                            "Voice control compatible",
                            "App-controlled dimming",
                            "Scheduling and automation",
                            "Energy efficient LED"
                        ]
                    },
                    {
                        "name": "Arlo Pro 4 Security Camera",
                        "category": "Smart Security",
                        "price": "199.99",
                        "brand": "Arlo",
                        "features": [
                            "2K HDR video quality",
                            "Wire-free installation",
                            "Color night vision",
                            "Two-way audio",
                            "Smart motion detection"
                        ]
                    }
                ]
                self.save_products_queue()
            
            # Load topics queue
            if os.path.exists('topics_queue.json'):
                with open('topics_queue.json', 'r') as f:
                    self.topics_queue = json.load(f)
            else:
                # Create default topics queue
                self.topics_queue = [
                    {
                        "title": "Smart Home Security Systems: Complete Buyer's Guide 2025",
                        "keywords": ["smart security", "home security", "security cameras", "smart locks"]
                    },
                    {
                        "title": "Best Smart Speakers for Every Budget in 2025",
                        "keywords": ["smart speakers", "voice assistants", "Alexa", "Google Assistant"]
                    },
                    {
                        "title": "How to Create the Perfect Smart Lighting Setup",
                        "keywords": ["smart lighting", "Philips Hue", "smart bulbs", "home automation"]
                    },
                    {
                        "title": "Smart Thermostats: Save Money and Energy in 2025",
                        "keywords": ["smart thermostat", "energy saving", "Nest", "Ecobee"]
                    }
                ]
                self.save_topics_queue()
                
        except Exception as e:
            logging.error(f"Error loading content queues: {e}")
    
    def save_products_queue(self):
        """Save products queue to JSON file"""
        try:
            with open('products_queue.json', 'w') as f:
                json.dump(self.products_queue, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving products queue: {e}")
    
    def save_topics_queue(self):
        """Save topics queue to JSON file"""
        try:
            with open('topics_queue.json', 'w') as f:
                json.dump(self.topics_queue, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving topics queue: {e}")
    
    def generate_daily_review(self):
        """Generate a daily product review"""
        if not self.products_queue:
            logging.warning("No products in queue for review generation")
            return
        
        try:
            # Get next product from queue
            product = self.products_queue.pop(0)
            logging.info(f"Generating review for: {product['name']}")
            
            # Generate review
            review_html = self.ai.generate_product_review(product)
            
            if review_html:
                # Save review
                filename = f"review-{product['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')}.html"
                success = self.ai.save_content(filename, review_html)
                
                if success:
                    logging.info(f"✅ Daily review generated: {filename}")
                    # Update homepage with new review (you can implement this)
                    self.update_homepage_featured_reviews(product, filename)
                else:
                    logging.error(f"Failed to save review: {filename}")
                    # Put product back in queue
                    self.products_queue.insert(0, product)
            else:
                logging.error(f"Failed to generate review for: {product['name']}")
                # Put product back in queue
                self.products_queue.insert(0, product)
            
            # Save updated queue
            self.save_products_queue()
            
        except Exception as e:
            logging.error(f"Error in daily review generation: {e}")
    
    def generate_weekly_article(self):
        """Generate a weekly blog article"""
        if not self.topics_queue:
            logging.warning("No topics in queue for article generation")
            return
        
        try:
            # Get next topic from queue
            topic_data = self.topics_queue.pop(0)
            logging.info(f"Generating article: {topic_data['title']}")
            
            # Generate article
            article_html = self.ai.generate_blog_article(
                topic_data['title'], 
                topic_data['keywords']
            )
            
            if article_html:
                # Save article
                filename = f"blog-{topic_data['title'].lower().replace(' ', '-').replace(':', '').replace('?', '')}.html"
                success = self.ai.save_content(filename, article_html)
                
                if success:
                    logging.info(f"✅ Weekly article generated: {filename}")
                    # Update homepage with new article (you can implement this)
                    self.update_homepage_blog_section(topic_data, filename)
                else:
                    logging.error(f"Failed to save article: {filename}")
                    # Put topic back in queue
                    self.topics_queue.insert(0, topic_data)
            else:
                logging.error(f"Failed to generate article: {topic_data['title']}")
                # Put topic back in queue
                self.topics_queue.insert(0, topic_data)
            
            # Save updated queue
            self.save_topics_queue()
            
        except Exception as e:
            logging.error(f"Error in weekly article generation: {e}")
    
    def update_homepage_featured_reviews(self, product, filename):
        """Update homepage with new featured review"""
        # This is a placeholder - implement based on your needs
        logging.info(f"Homepage updated with new review: {product['name']}")
    
    def update_homepage_blog_section(self, topic_data, filename):
        """Update homepage with new blog article"""
        # This is a placeholder - implement based on your needs
        logging.info(f"Homepage updated with new article: {topic_data['title']}")
    
    def health_check(self):
        """Perform system health check"""
        try:
            logging.info("🔍 Performing health check...")
            
            # Check if queues have content
            if len(self.products_queue) < 5:
                logging.warning(f"Products queue low: {len(self.products_queue)} items remaining")
            
            if len(self.topics_queue) < 3:
                logging.warning(f"Topics queue low: {len(self.topics_queue)} items remaining")
            
            # Check disk space
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_gb = free // (1024**3)
            
            if free_gb < 1:
                logging.warning(f"Low disk space: {free_gb}GB remaining")
            
            # Check if website files exist
            required_files = ['index.html', 'styles.css', 'script.js']
            for file in required_files:
                if not os.path.exists(file):
                    logging.error(f"Missing required file: {file}")
            
            logging.info("✅ Health check completed")
            
        except Exception as e:
            logging.error(f"Error in health check: {e}")
    
    def backup_content(self):
        """Create backup of generated content"""
        try:
            import shutil
            from datetime import datetime
            
            backup_dir = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup HTML files
            for file in os.listdir('.'):
                if file.endswith('.html'):
                    shutil.copy2(file, backup_dir)
            
            # Backup queue files
            if os.path.exists('products_queue.json'):
                shutil.copy2('products_queue.json', backup_dir)
            if os.path.exists('topics_queue.json'):
                shutil.copy2('topics_queue.json', backup_dir)
            
            logging.info(f"✅ Backup created: {backup_dir}")
            
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
    
    def start_scheduler(self):
        """Start the automation scheduler"""
        logging.info("🚀 Starting TechReview Hub Automation Scheduler")
        
        # Schedule daily tasks
        schedule.every().day.at("09:00").do(self.generate_daily_review)
        schedule.every().day.at("12:00").do(self.health_check)
        
        # Schedule weekly tasks
        schedule.every().monday.at("10:00").do(self.generate_weekly_article)
        schedule.every().sunday.at("23:00").do(self.backup_content)
        
        logging.info("📅 Scheduled tasks:")
        logging.info("  - Daily review generation: 9:00 AM")
        logging.info("  - Daily health check: 12:00 PM")
        logging.info("  - Weekly article generation: Monday 10:00 AM")
        logging.info("  - Weekly backup: Sunday 11:00 PM")
        
        # Run scheduler
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logging.info("🛑 Scheduler stopped by user")
                break
            except Exception as e:
                logging.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

def main():
    """Main function"""
    print("🤖 TechReview Hub Automation Scheduler")
    print("=====================================")
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Please set your OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize scheduler
    scheduler = AutomationScheduler(api_key)
    
    print("\nOptions:")
    print("1. Start automated scheduler")
    print("2. Generate content now (manual)")
    print("3. View content queues")
    print("4. Add content to queues")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        print("\n🚀 Starting automated scheduler...")
        print("Press Ctrl+C to stop")
        scheduler.start_scheduler()
    
    elif choice == '2':
        print("\n🔧 Manual content generation:")
        print("1. Generate product review")
        print("2. Generate blog article")
        
        manual_choice = input("Choose (1-2): ").strip()
        
        if manual_choice == '1':
            scheduler.generate_daily_review()
        elif manual_choice == '2':
            scheduler.generate_weekly_article()
        else:
            print("❌ Invalid choice")
    
    elif choice == '3':
        print(f"\n📋 Content Queues:")
        print(f"Products in queue: {len(scheduler.products_queue)}")
        for i, product in enumerate(scheduler.products_queue[:3]):
            print(f"  {i+1}. {product['name']}")
        
        print(f"\nTopics in queue: {len(scheduler.topics_queue)}")
        for i, topic in enumerate(scheduler.topics_queue[:3]):
            print(f"  {i+1}. {topic['title']}")
    
    elif choice == '4':
        print("\n➕ Add content to queues (feature coming soon)")
        print("Edit products_queue.json and topics_queue.json manually for now")
    
    elif choice == '5':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()