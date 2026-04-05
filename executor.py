"""
Professional Traffic Simulation - REAL Chrome Profile Integration
Version: 4.1.0 - Optimized for Direct Profile Path
"""

import os
import time
import random
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================================================================
# Configuration
# ============================================================================

@dataclass
class ProfileConfig:
    """Real Chrome profile configuration"""
    # معرف المجلد من جوجل درايف
    folder_id: str = "1bLSRdF8_BY-egYAZ7pO0Ae9taTtewXwa"
    # اسم المجلد المحلي الذي سيتم التنزيل فيه
    local_profile_path: str = "user_data" 

class ChromeProfileManager:
    """إدارة تنزيل ملف التعريف الحقيقي"""
    def __init__(self, config: ProfileConfig = ProfileConfig()):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def download_profile_from_drive(self) -> bool:
        """تنزيل المجلد باستخدام gdown"""
        try:
            import gdown
            url = f"https://drive.google.com/drive/folders/{self.config.folder_id}"
            self.logger.info(f"⏳ Downloading profile from Drive...")
            
            # تنزيل المجلد بالكامل
            gdown.download_folder(url, output=self.config.local_profile_path, quiet=False, use_cookies=False)
            
            # التحقق من وجود ملف History (الذي رأيناه في الصور)
            history_file = Path(self.config.local_profile_path) / "History"
            if history_file.exists():
                self.logger.info(f"✅ Profile verified. History size: {history_file.stat().st_size / 1024 / 1024:.2f} MB")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Download failed: {e}")
            return False

class AdvancedHumanSimulator:
    """محاكاة السلوك البشري باستخدام ملف تعريف حقيقي"""
    def __init__(self, profile_path: str):
        self.profile_path = os.path.abspath(profile_path)
        self.logger = logging.getLogger(__name__)

    def create_stealth_driver(self) -> webdriver.Chrome:
        options = Options()
        
        # --- الإعدادات الحيوية للمسارات ---
        # استخدام المجلد الذي يحتوي على ملف History مباشرة
        options.add_argument(f"--user-data-dir={self.profile_path}")
        # إجبار الكروم على اعتبار الجذر هو ملف التعريف (لأن ملفاتك ليست داخل مجلد Default)
        options.add_argument(f"--profile-directory=.") 
        
        # --- إعدادات التخفي (Stealth) ---
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # إعدادات إضافية للاستقرار في بيئة السيرفر (GitHub Actions)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        # خيارات تفضيلات المستخدم لتجنب النوافذ المنبثقة
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # إخفاء خاصية السيلينيوم من المتصفح
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def simulate_natural_browsing(self, driver: webdriver.Chrome, target_url: str):
        """دورة التصفح الكاملة"""
        try:
            # 1. البحث في جوجل أولاً (لإضفاء الشرعية)
            queries = ["dyson airwrap i.d. review 2025", "intelligent hair styler dyson"]
            query = random.choice(queries)
            
            self.logger.info(f"🔍 Searching Google for: {query}")
            driver.get("https://www.google.com")
            time.sleep(random.uniform(2, 4))
            
            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
            for char in query:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
            search_box.submit()
            
            # 2. الانتقال للهدف (Target)
            time.sleep(random.uniform(3, 5))
            self.logger.info(f"🎯 Navigating to target: {target_url}")
            driver.get(target_url)
            
            # 3. محاكاة القراءة (Scrolling)
            self._natural_scroll(driver)
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Simulation error: {e}")
            return False

    def _natural_scroll(self, driver):
        """محاكاة سكرول بشري غير منتظم"""
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_pos = 0
        while current_pos < total_height:
            step = random.randint(200, 500)
            current_pos += step
            driver.execute_script(f"window.scrollTo(0, {current_pos});")
            time.sleep(random.uniform(2, 5))
            # تحديث الطول في حال كان هناك لودينج
            total_height = driver.execute_script("return document.body.scrollHeight")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    # 1. إدارة ملف التعريف
    manager = ChromeProfileManager()
    if not manager.download_profile_from_drive():
        print("❌ Could not load profile. Check folder ID or gdown installation.")
        return

    # 2. بدء المحاكاة
    simulator = AdvancedHumanSimulator(manager.config.local_profile_path)
    driver = simulator.create_stealth_driver()
    
    try:
        target = "https://elite-beauty-lab.github.io/Dyson-Airwrap-i.d.-Intelligent-Hair-Styler/"
        success = simulator.simulate_natural_browsing(driver, target)
        
        if success:
            print("✅ MISSION ACCOMPLISHED: Traffic sent with real profile data.")
            # البقاء في الصفحة لفترة لمحاكاة وقت القراءة (Dwell Time)
            time.sleep(random.randint(40, 70))
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
