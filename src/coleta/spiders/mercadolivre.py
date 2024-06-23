import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    # request dentro do site
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

    # Para não ter o acesso bloqueado, vamos limitar o número de paginas
    page_count = 1
    max_pages = 10

    def parse(self, response):
        #pegar o bloco onde estão os produtos
        products = response.css('div.ui-search-result__content')
        
        for product in products:
            prices = products[0].css('span.andes-money-amount__fraction::text').getall()           
            cents = products[0].css('span.andes-money-amount__cents::text').getall()

            #pegar varias informações de produtos
            yield {
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None, #se o preço estiver > 0 retorna null
                'old_price_centavos': cents[0] if len(prices) > 0 else None,
                'new_price_reais': prices[1] if len(prices) > 1 else None,
                'new_price_centavos': cents[1] if len(prices) > 1 else None,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get()
            }

        # IF para percorrer até a decima pagina
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)