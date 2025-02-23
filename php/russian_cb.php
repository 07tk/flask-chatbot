<?php
// Ввод пользователя с формы или другого источника
$user_message = "Привет, чат-бот!";

// URL API Python Flask
$python_api_url = 'http://3.144.89.161:80/chat';  // Замените на URL вашего Python Flask API

// Данные, которые отправляются в POST запросе
$data = array('message' => $user_message);

// Инициализация cURL
$ch = curl_init($python_api_url);

// Установка параметров cURL
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  // Возвращаем ответ как строку
curl_setopt($ch, CURLOPT_POST, true);  // Устанавливаем метод запроса POST
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));  // Отправляем данные как JSON
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',  // Устанавливаем тип контента как JSON
));

// Выполнение запроса cURL и получение ответа
$response = curl_exec($ch);

// Проверка на ошибки cURL
if ($response === false) {
    echo "Ошибка cURL: " . curl_error($ch);
} else {
    // Декодируем JSON ответ от Python API
    $response_data = json_decode($response, true);
    echo "Ответ чат-бота: " . $response_data['response'];
}

// Закрытие сессии cURL
curl_close($ch);
?>
