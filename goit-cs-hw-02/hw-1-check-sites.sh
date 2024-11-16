#!/bin/bash

# Масив з URL вебсайтів для перевірки
websites=("https://google.com" "https://facebook.com" "https://twitter.com")

# Ім'я файлу логів
log_file="website_status.log"

# Очищаємо файл логів перед записом нових даних
> "$log_file"

# Перевіряємо кожен сайт зі списку
for website in "${websites[@]}"
do
  # Використовуємо curl для перевірки статусу сайту та опрацьовуємо переадресацію
  http_status=$(curl -o /dev/null -s -w "%{http_code}" -L "$website")

  # Перевіряємо чи статус-код дорівнює 200 (успішна відповідь)
  if [ "$http_status" -eq 200 ]; then
    echo "$website is UP" | tee -a "$log_file"
  else
    echo "$website is DOWN" | tee -a "$log_file"
  fi
done

# Виводимо повідомлення про запис результатів у файл логів
echo "Результати записано у файл логів: $log_file"