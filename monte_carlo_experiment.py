import numpy as np
import matplotlib.pyplot as plt
import math

def inside_circle(x, y, center_x, center_y, radius):
    return (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2

def monte_carlo_area(num_points, region, circles):
    x1, x2, y1, y2 = region
    # Случайная генерация точек (равномерно по прямоугольнику)
    rand_points = np.random.uniform(low=[x1, y1], high=[x2, y2], size=(num_points, 2))

    mask = np.ones(num_points, dtype=bool)
    for (cx, cy, r) in circles:
        mask &= inside_circle(rand_points[:, 0], rand_points[:, 1], cx, cy, r)

    ratio = np.sum(mask) / num_points
    rect_area = (x2 - x1) * (y2 - y1)
    return rect_area * ratio

circles = [
    (1.0, 1.0, 1.0),
    (1.5, 2.0, math.sqrt(5) / 2),
    (2.0, 1.5, math.sqrt(5) / 2)
]

# Прямоугольники для генерации
wide_box = (0, 3, 0, 3)   # широкая область
tight_box = (2 - math.sqrt(5) / 2, 2, 2 - math.sqrt(5) / 2, 2)  # "плотная" область

# Точное значение площади (из аналитического решения)
S_exact = 0.25 * math.pi + 1.25 * math.asin(0.8) - 1

N_values = np.arange(100, 100001, 500)
area_wide, area_tight = [], []
error_wide, error_tight = [], []

for N in N_values:
    s_wide = monte_carlo_area(N, wide_box, circles)
    s_tight = monte_carlo_area(N, tight_box, circles)

    area_wide.append(s_wide)
    area_tight.append(s_tight)

    error_wide.append(abs(s_wide - S_exact) / S_exact * 100)
    error_tight.append(abs(s_tight - S_exact) / S_exact * 100)

# График 1 — приближённая площадь
plt.figure(figsize=(10, 6))
plt.plot(N_values, area_wide, color='pink', label='Широкая область')
plt.plot(N_values, area_tight, color='crimson', label='Узкая область')
plt.axhline(S_exact, color='black', linestyle='--', label='Точное значение')
plt.title('Сходимость приближённой площади при увеличении N')
plt.xlabel('Количество точек N')
plt.ylabel('Площадь фигуры')
plt.legend()
plt.grid(True)
plt.show()

# График 2 — относительная ошибка (%)
plt.figure(figsize=(10, 6))
plt.plot(N_values, error_wide, color='pink', label='Широкая область')
plt.plot(N_values, error_tight, color='crimson', label='Узкая область')
plt.title('Относительная погрешность оценки площади')
plt.xlabel('Количество точек N')
plt.ylabel('Ошибка, %')
plt.legend()
plt.grid(True)
plt.show()

