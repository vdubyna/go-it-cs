-- 1. Отримати всі завдання певного користувача
SELECT *
FROM tasks
WHERE user_id = 1;

-- 2. Вибрати завдання за певним статусом
-- Замініть 'new' на потрібний статус
SELECT *
FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання
-- Замініть 5 на id завдання, яке потрібно оновити
-- Замініть 'in progress' на потрібний статус
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 5;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT *
FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task', 'Description of the task', 1, 3);

-- 6. Отримати всі завдання, які ще не завершено
SELECT *
FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити конкретне завдання
DELETE
FROM tasks
WHERE id = 10;

-- 8. Знайти користувачів з певною електронною поштою
SELECT *
FROM users
WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача
UPDATE users
SET fullname = 'Updated Name'
WHERE id = 2;

-- 10. Отримати кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) AS task_count
FROM status s
         LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
-- Замініть '%@gmail.com' на потрібний домен
SELECT t.*
FROM tasks AS t
         JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@gmail.com';

-- 12. Отримати список завдань, що не мають опису
SELECT *
FROM tasks
WHERE description IS NULL;

-- 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
-- Замініть 'in progress' на потрібний статус
SELECT u.fullname, t.title
FROM users AS u
         JOIN tasks t ON u.id = t.user_id
         JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users AS u
         LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id;