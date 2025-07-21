import asyncio
import time
import logging
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PerplexityAutomator:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.playwright = None
        
    async def setup_browser(self):
        """Initialize browser with stealth settings"""
        try:
            self.playwright = await async_playwright().__aenter__()
            
            # Advanced stealth configuration
            browser_options = {
                'headless': True,
                'args': [
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                ]
            }
            
            self.browser = await self.playwright.chromium.launch(**browser_options)
            
            # Context with realistic settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            # Inject stealth scripts
            await self.context.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            ''')
            
            logger.info("Browser setup completed successfully")
            
        except Exception as e:
            logger.error(f"Browser setup failed: {str(e)}")
            raise

    async def search_perplexity(self, prompt: str, timeout: int = 30) -> Dict[str, Any]:
        """Automate Perplexity search with multiple fallback strategies"""
        if not self.context:
            await self.setup_browser()
            
        page = None
        start_time = time.time()
        
        try:
            page = await self.context.new_page()
            
            # Block unnecessary resources for faster loading
            await page.route("**/*.{jpg,jpeg,png,gif,svg,woff,woff2}", lambda route: route.abort())
            await page.route("**/analytics*", lambda route: route.abort())
            await page.route("**/ads*", lambda route: route.abort())
            
            # Navigate to Perplexity
            logger.info("Navigating to Perplexity.AI")
            await page.goto("https://www.perplexity.ai", wait_until="networkidle", timeout=timeout*1000)
            
            # Wait for page to fully load
            await page.wait_for_timeout(2000)
            
            # Multiple selector strategies for search input
            search_selectors = [
                'textarea[placeholder*="Ask anything"]',
                'textarea[placeholder*="Ask"]',
                'textarea[data-testid="search-input"]',
                'textarea.search-input',
                'input[type="text"]',
                '[data-testid="search-input"]'
            ]
            
            search_element = None
            for selector in search_selectors:
                try:
                    search_element = await page.wait_for_selector(selector, timeout=5000)
                    if search_element:
                        logger.info(f"Found search element with selector: {selector}")
                        break
                except:
                    continue
            
            if not search_element:
                raise Exception("Could not find search input element")
            
            # Click and fill the search input
            await search_element.click()
            await page.wait_for_timeout(1000)
            
            # Type with human-like delays
            await search_element.fill("")  # Clear first
            for char in prompt:
                await search_element.type(char, delay=50)
            
            # Submit the search
            await page.keyboard.press("Enter")
            logger.info(f"Search submitted for prompt: {prompt[:50]}...")
            
            # Wait for results with multiple strategies
            result_selectors = [
                '[data-testid="copilot-answer"]',
                '.prose',
                '[data-testid="answer"]',
                '.answer-content',
                '.result-content'
            ]
            
            answer_element = None
            for selector in result_selectors:
                try:
                    answer_element = await page.wait_for_selector(selector, timeout=timeout*1000)
                    if answer_element:
                        logger.info(f"Found answer element with selector: {selector}")
                        break
                except:
                    continue
            
            if not answer_element:
                # Fallback: wait and get page content
                await page.wait_for_timeout(10000)
                page_content = await page.content()
                if "answer" in page_content.lower() or "result" in page_content.lower():
                    # Try to extract text from main content area
                    main_content = await page.locator('main, .main-content, #main').first.inner_text()
                    if main_content:
                        return {
                            'success': True,
                            'answer': main_content.strip()[:2000],  # Limit length
                            'execution_time': round(time.time() - start_time, 2),
                            'method': 'fallback_main_content'
                        }
                
                raise Exception("Could not find answer element after search")
            
            # Extract the answer text
            answer_text = await answer_element.inner_text()
            
            # Try to extract sources if available
            sources = []
            try:
                source_elements = await page.locator('a[href*="http"]').all()
                for source in source_elements[:5]:  # Limit to 5 sources
                    href = await source.get_attribute('href')
                    text = await source.inner_text()
                    if href and text and len(text.strip()) > 10:
                        sources.append({'url': href, 'title': text.strip()})
            except Exception as e:
                logger.warning(f"Could not extract sources: {str(e)}")
            
            execution_time = round(time.time() - start_time, 2)
            
            result = {
                'success': True,
                'answer': answer_text.strip(),
                'sources': sources,
                'execution_time': execution_time,
                'prompt': prompt
            }
            
            logger.info(f"Search completed successfully in {execution_time}s")
            return result
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'execution_time': round(time.time() - start_time, 2),
                'prompt': prompt
            }
        finally:
            if page:
                await page.close()

    async def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.__aexit__(None, None, None)
            logger.info("Browser cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")