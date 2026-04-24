from src.scrapers.moodys_scraper import MoodysScraper
from src.scrapers.fitch_scraper import FitchScraper
from src.scrapers.sp_scraper import SPScraper
from src.utils.data_processor import DataProcessor
import schedule
import time
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_scraping():
    """Ejecuta el proceso completo de scraping y procesamiento"""
    logger.info("🚀 Iniciando proceso de scraping...")
    
    # Inicializar scrapers
    moodys = MoodysScraper()
    fitch = FitchScraper()
    sp = SPScraper()
    processor = DataProcessor()
    
    # Diccionario para almacenar resultados
    all_news = {}
    
    try:
        # Scraping de cada fuente
        logger.info("Scraping Moody's...")
        moodys_news = moodys.scrape_news()
        if not moodys_news.empty:
            all_news['Moody\'s'] = moodys_news
            processor.save_raw_data(moodys_news, 'moodys')
            logger.info(f"✅ Moody's: {len(moodys_news)} noticias encontradas")
        
        logger.info("Scraping Fitch...")
        fitch_news = fitch.scrape_research()
        if not fitch_news.empty:
            all_news['Fitch'] = fitch_news
            processor.save_raw_data(fitch_news, 'fitch')
            logger.info(f"✅ Fitch: {len(fitch_news)} noticias encontradas")
        
        logger.info("Scraping S&P...")
        sp_news = sp.scrape_insights()
        if not sp_news.empty:
            all_news['S&P Global'] = sp_news
            processor.save_raw_data(sp_news, 'sp')
            logger.info(f"✅ S&P: {len(sp_news)} noticias encontradas")
        
        # Procesar datos combinados
        if all_news:
            logger.info("Procesando datos...")
            processed_df = processor.process_news_data(all_news)
            stats = processor.generate_summary_stats(processed_df)
            logger.info(f"📊 Procesamiento completado: {len(processed_df)} noticias en total")
        else:
            logger.warning("⚠️ No se encontraron noticias nuevas")
    
    except Exception as e:
        logger.error(f"❌ Error en el proceso: {e}")

def run_dashboard():
    """Ejecuta el dashboard"""
    from src.dashboard.app import app
    logger.info("📊 Iniciando dashboard...")
    app.run_server(debug=False, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    # Ejecutar scraping inicial
    run_scraping()
    
    # Programar ejecución automática cada 6 horas
    schedule.every(6).hours.do(run_scraping)
    
    # Para ejecutar el dashboard descomentar la línea siguiente
    # run_dashboard()
    
    # Mantener el script corriendo
    logger.info("⏰ Programador iniciado. Ejecutando scraping cada 6 horas")
    while True:
        schedule.run_pending()
        time.sleep(60)