# from stem.control import Controller
#
# onion_address = "fdy6szsebmu56buihzafvcquorjxvu73625ckrqz6sfyv5jrrgnnzlid.onion"
#
# with Controller.from_port(port=9051) as controller:
#     controller.authenticate()
#     descriptor = controller.get_hidden_service_descriptor(onion_address)
#     print("Descriptor lifetime:", descriptor.lifetime)






import numpy as np
import matplotlib.pyplot as plt

# Parametry:
p = 0.0523    # prawdopodobieństwo przejęcia 1 obwodu
h_max = 24    # do ilu godzin chcemy rysować (np. 24h)
step_minutes = 10  # chcemy co 10 minut

# 1. Generujemy wektor czasu w minutach z krokiem 10 minut:
time_minutes = np.arange(0, h_max*60 + 1, step_minutes)
# 2. Zamieniamy minuty na godziny:
time_hours = time_minutes / 60.0

# 3. Obliczamy liczbę obwodów po t godzinach:
#    T(t) = 6 obwodów na godzinę * t godzin
T_values = 6 * time_hours

# 4. Obliczamy prawdopodobieństwo: 1 - (1 - p)^T(t)
prob_values = 1 - (1 - p)**T_values

# 5. Rysujemy wykres punktowy (scatter):
plt.figure(figsize=(8, 5))
plt.scatter(time_hours, prob_values)
plt.xlabel('Czas (godziny)')
plt.ylabel('Prawdopodobieństwo')
plt.title('Prawdopodobieństwo deanonimizacji w zależności od czasu')
plt.grid(True)
plt.show()






# import numpy as np
# import matplotlib.pyplot as plt
#
# p_g = 0.2286  # Prawdopodobieństwo trafienia na guard niemiecki
#
# # Załóżmy, że chcemy pokazać do 10 "okresów" (tj. 600 dni)
# k_max = 20
# k_values = np.arange(0, k_max+1, 1)  # 0, 1, 2, ..., 10
#
# # P(k) = 1 - (1 - p_g)^k
# prob_values = 1 - (1 - p_g)**k_values
#
# # Przeliczmy to też na dni, by mieć etykiety: 1 okres = 60 dni
# days_values = 60 * k_values
#
# plt.figure(figsize=(8, 5))
# plt.scatter(days_values, prob_values, marker='o', label='Prawdopodobieństwo przejęcia')
# plt.title('Prawdopodobieństwo przejęcia guard relay w kolejnych okresach 60-dniowych')
# plt.xlabel('Czas (dni)')
# plt.ylabel('Prawdopodobieństwo')
# plt.grid(True)
# plt.legend()
# plt.show()
