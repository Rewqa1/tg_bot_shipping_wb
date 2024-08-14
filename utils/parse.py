from datetime import datetime


async def parse_income(data, date_start, date_end):
    income = []
    sizes = set()

    for item in data:
        article = item['supplierArticle']
        size = item['techSize']
        quantity = item['quantity']
        date_close = item['dateClose']
        warehouse_name = item['warehouseName']
        status = item['status']
        date_close_object = datetime.strptime(date_close, "%Y-%m-%dT%H:%M:%S")

        if (date_start <= date_close_object <= date_end) and status == 'Принято':
            sizes.add(size)
            warehouse_found = next((w for w in income if w['warehouseName'] == warehouse_name), None)

            if warehouse_found:
                stock_income_articles = warehouse_found['articles']
            else:
                stock_income_articles = []
                warehouse_found = {'warehouseName': warehouse_name, 'fullIncomeQuantityStock': 0, 'articles': stock_income_articles}
                income.append(warehouse_found)

            article_found = next((a for a in stock_income_articles if a['article'] == article and a['size'] == size), None)

            if article_found:

                article_found['quantity'] = article_found.get('quantity', 0) + quantity


            else:

                new_article = {'article': article, 'size': size, 'quantity': quantity}
                stock_income_articles.append(new_article)

            warehouse_found['fullIncomeQuantityStock'] += quantity
    income = sort_articles(income, sizes)
    all_income = get_all_articles(income)
    return income, all_income

def get_size_income(sizes):
    if "XS" in sizes:
        return {"XS": 1, "S": 2, "M": 3, "L": 4}
    return {"S": 1, "M": 2, "L": 3}

def sort_articles(income, sizes):
    sorted_income = sorted(income, key=lambda x: x['fullIncomeQuantityStock'], reverse=True)

    size_income = get_size_income(sizes)

    for warehouse in sorted_income:
        warehouse['articles'] = sorted(warehouse['articles'],
                                       key=lambda x: (x['article'],
                                                      size_income.get(x['size'], 0)))
    return sorted_income

def get_all_articles(incomes):
    all_income = {}
    full_quantity = 0

    for warehouse in incomes:
        full_quantity += warehouse['fullIncomeQuantityStock']
        for item in warehouse['articles']:
            article = item['article']
            size = item['size']
            quantity = item['quantity']

            if article + size not in all_income:
                all_income[article + size] = quantity

            else:
                all_income[article + size] += quantity


    all_income['fullQuantity'] = full_quantity

    return all_income