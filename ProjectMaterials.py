import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Material:
    """Класс для представления материала"""
    name: str
    category: str
    prices: Dict[str, float]  

@dataclass
class OrderItem:
    """Класс для позиции в заказе"""
    material_name: str
    category: str
    region: str
    original_price: float
    final_price: float
    discount_applied: bool = False

class MaterialCatalog:
    """Класс для работы с каталогом материалов"""
    
    def __init__(self):
        self.materials: List[Material] = []
        self.regions: List[str] = []
        self._initialize_catalog()
    
    def _initialize_catalog(self):
        """Инициализация каталога с тестовыми данными"""
        materials_data = [
            
            ("Утеплитель Роквул Скандик 50 мм", "Утеплитель", {"СПБ": 1075, "МСК": 1100, "КРД": 950}),
            ("Утеплитель Кнауф ТеплоКНАУФ 50 мм", "Утеплитель", {"СПБ": 860, "МСК": 900, "КРД": 1300}),
            ("Утеплитель Технониколь 50 мм", "Утеплитель", {"СПБ": 920, "МСК": 890, "КРД": 880}),
            
            ("Газобетон СК D400 100х250х625 мм", "Газобетон", {"СПБ": 450, "МСК": 430, "КРД": 420}),
            ("Газобетон ЛСР D400 100х250х625 мм", "Газобетон", {"СПБ": 580, "МСК": 550, "КРД": 580}),
            ("Газобетон Bonolit D400 100х250х625 мм", "Газобетон", {"СПБ": 520, "МСК": 500, "КРД": 490}),
            
            ("Кирпич керамический лицевой", "Кирпич", {"СПБ": 85, "МСК": 82, "КРД": 75}),
            ("Кирпич силикатный белый", "Кирпич", {"СПБ": 65, "МСК": 62, "КРД": 58}),
            ("Кирпич клинкерный", "Кирпич", {"СПБ": 120, "МСК": 115, "КРД": 110}),
            
            ("Цемент М500 50 кг", "Цемент", {"СПБ": 550, "МСК": 520, "КРД": 500}),
            ("Цемент М400 50 кг", "Цемент", {"СПБ": 480, "МСК": 460, "КРД": 440}),
            
            ("Гипсокартон Кнауф 2500x1200x12.5 мм", "Гипсокартон", {"СПБ": 450, "МСК": 430, "КРД": 410}),
            ("Гипсокартон Волма 2500x1200x12.5 мм", "Гипсокартон", {"СПБ": 380, "МСК": 360, "КРД": 340}),
        ]
        
        for name, category, prices in materials_data:
            self.materials.append(Material(name, category, prices))
            for region in prices.keys():
                if region not in self.regions:
                    self.regions.append(region)
        
        self.regions.sort()
    
    def get_materials_by_region(self, region: str) -> List[Material]:
        """Получить все материалы для указанного региона"""
        return [m for m in self.materials if region in m.prices]
    
    def get_cheapest_in_category(self, category: str, region: str) -> Optional[Material]:
        """Найти самый дешевый товар в категории для региона"""
        category_materials = [m for m in self.materials if m.category == category and region in m.prices]
        if not category_materials:
            return None
        return min(category_materials, key=lambda m: m.prices[region])

class OrderManager:
    """Класс для управления заказами"""
    
    def __init__(self, catalog: MaterialCatalog):
        self.catalog = catalog
        self.current_order: Optional[OrderItem] = None
        self.orders_dir = "orders"
        
        if not os.path.exists(self.orders_dir):
            os.makedirs(self.orders_dir)
    
    def create_order(self, material: Material, region: str) -> OrderItem:
        """Создать позицию заказа"""
        return OrderItem(
            material_name=material.name,
            category=material.category,
            region=region,
            original_price=material.prices[region],
            final_price=material.prices[region],
            discount_applied=False
        )
    
    def apply_retention_logic(self, order: OrderItem) -> OrderItem:
        """Применить логику удержания клиента"""
        material = next((m for m in self.catalog.materials if m.name == order.material_name), None)
        if not material:
            return order
        
        cheapest = self.catalog.get_cheapest_in_category(material.category, order.region)
        
        if cheapest and cheapest.name == material.name:
            order.final_price = order.original_price * 0.95
            order.discount_applied = True
        else:
            print(f"\n Мы можем предложить вам более выгодный вариант:")
            print(f"   {cheapest.name} - {cheapest.prices[order.region]} руб.")
            print(f"   (вместо {order.original_price} руб.)")
            
            response = input("   Хотите заменить товар на этот? (y/n): ").lower()
            if response == 'y':
                order.material_name = cheapest.name
                order.original_price = cheapest.prices[order.region]
                order.final_price = cheapest.prices[order.region]
        
        return order
    
    def save_order(self, order: OrderItem):
        """Сохранить заказ в JSON файл"""
        order_data = {
            "order_id": f"ORD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "material": {
                "name": order.material_name,
                "category": order.category
            },
            "region": order.region,
            "pricing": {
                "original_price": order.original_price,
                "final_price": order.final_price,
                "discount_applied": order.discount_applied,
                "discount_percent": 5 if order.discount_applied else 0
            }
        }
        
        filename = f"{self.orders_dir}/order_{order_data['order_id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(order_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nЗаказ сохранен в файл: {filename}")
        return filename

class ConsoleApp:
    """Консольное приложение"""
    
    def __init__(self):
        self.catalog = MaterialCatalog()
        self.order_manager = OrderManager(self.catalog)
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Вывод заголовка"""
        print("=" * 60)
        print(f"🏗️  {title}")
        print("=" * 60)
    
    def select_region(self) -> Optional[str]:
        """Выбор региона"""
        self.print_header("ВЫБОР РЕГИОНА")
        
        for i, region in enumerate(self.catalog.regions, 1):
            print(f"{i}. {region}")
        
        try:
            choice = int(input("\nВыберите номер региона: "))
            if 1 <= choice <= len(self.catalog.regions):
                return self.catalog.regions[choice - 1]
            else:
                print("Неверный номер региона")
                return None
        except ValueError:
            print("Пожалуйста, введите число")
            return None
    
    def select_material(self, region: str) -> Optional[Material]:
        """Выбор материала"""
        self.print_header(f"ВЫБОР МАТЕРИАЛА (Регион: {region})")
        
        materials = self.catalog.get_materials_by_region(region)
        
        categories = {}
        for material in materials:
            if material.category not in categories:
                categories[material.category] = []
            categories[material.category].append(material)
        
        material_list = []
        index = 1
        
        for category, cat_materials in categories.items():
            print(f"\n{category}:")
            for material in cat_materials:
                print(f"   {index}. {material.name} - {material.prices[region]} руб.")
                material_list.append(material)
                index += 1
        
        try:
            choice = int(input(f"\nВыберите номер материала (1-{len(material_list)}): "))
            if 1 <= choice <= len(material_list):
                selected = material_list[choice - 1]
                print(f"\nВы выбрали: {selected.name}")
                return selected
            else:
                print("Неверный номер материала")
                return None
        except ValueError:
            print("Пожалуйста, введите число")
            return None
    
    def show_order(self, order: OrderItem):
        """Отображение заказа"""
        self.print_header("ТЕКУЩИЙ ЗАКАЗ")
        print(f"Регион: {order.region}")
        print(f"Товар: {order.material_name}")
        print(f"Категория: {order.category}")
        print(f"Цена: {order.final_price:.2f} руб.")
        if order.discount_applied:
            print(f"Применена скидка 5%! (было {order.original_price:.2f} руб.)")
        print("-" * 60)
    
    def run(self):
        """Основной цикл приложения"""
        while True:
            self.clear_screen()
            self.print_header("СИСТЕМА ФОРМИРОВАНИЯ ЗАЯВОК")
            print("1. Создать новую заявку")
            print("2. Выйти")
            
            choice = input("\nВыберите действие: ")
            
            if choice == "2":
                print("\nДо свидания!")
                break
            
            if choice == "1":
                region = self.select_region()
                if not region:
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                material = self.select_material(region)
                if not material:
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                order = self.order_manager.create_order(material, region)
                self.show_order(order)
                
                confirm = input("\nОформляем заявку? (y/n): ").lower()
                
                if confirm == 'y':
                    self.order_manager.save_order(order)
                    input("\nНажмите Enter для продолжения...")
                else:
                    print("\nПрименяем специальное предложение...")
                    improved_order = self.order_manager.apply_retention_logic(order)
                    
                    self.show_order(improved_order)
                    
                    final_confirm = input("\nОформляем заявку с новым предложением? (y/n): ").lower()
                    if final_confirm == 'y':
                        self.order_manager.save_order(improved_order)
                    else:
                        print("\nЗаказ отменен")
                    
                    input("\nНажмите Enter для продолжения...")
            else:
                print("Неверный выбор")
                input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    app = ConsoleApp()
    app.run()