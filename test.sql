-- データベースを選択
USE hbnb_dev_db;

-- States テーブルにデータを追加
INSERT INTO states (id, created_at, updated_at, name) 
VALUES ('state_id_1', NOW(), NOW(), 'California'),
VALUES ('state_id_2', NOW(), NOW(), 'New York');

-- Cities テーブルにデータを追加
INSERT INTO cities (id, created_at, updated_at, name, state_id) 
VALUES ('city_id_1', NOW(), NOW(), 'San Francisco', 'state_id_1'),
	('city_id_2', NOW(), NOW(), 'Los Angeles', 'state_id_1'),
	('city_id_3', NOW(), NOW(), 'New York', 'state_id_2');

-- Users テーブルにデータを追加
INSERT INTO users (id, created_at, updated_at, email, password, first_name, last_name) 
VALUES ('user_id_1', NOW(), NOW(), 'user@example.com', MD5('password'), 'John', 'Doe');

-- Places テーブルにデータを追加
INSERT INTO places (id, created_at, updated_at, city_id, user_id, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude, image) 
VALUES ('place_id_1', NOW(), NOW(), 'city_id_1', 'user_id_1', 'Cozy Apartment', 'A cozy place to stay in the heart of the city.', 2, 1, 4, 100, 37.7749, -122.4194, 'image_url'),
	('place_id_2', NOW(), NOW(), 'city_id_2', 'user_id_1', 'Hotel LOS', 'Belle view Hotel to stay in the heart of the city.', 2, 1, 4, 100, 37.7749, -122.4194, 'image_url'),
	('place_id_3', NOW(), NOW(), 'city_id_2', 'user_id_1', 'MOTEL Dodgers', 'It is not far from the center of the city, and there is a downtown area and other amenities nearby.', 3, 1, 5, 100, 37.7749, -122.4194, 'image_url'),
	('place_id_4', NOW(), NOW(), 'city_id_3', 'user_id_1', 'New York Hotel Regency', 'A hotel offering the highest level of luxury with a 3-star restaurant, bar, and exclusive spa', 2, 2, 2, 1000, 37.7749, -122.4194, 'image_url');

-- Reviews テーブルにデータを追加
INSERT INTO reviews (id, created_at, updated_at, place_id, user_id, text) 
VALUES ('review_id_1', NOW(), NOW(), 'place_id_1', 'user_id_1', 'Great place! Had a wonderful time.'),
	('review_id_2', NOW(), NOW(), 'place_id_2', 'user_id_1', 'The staff was very friendly and the room was beautiful!'),
        ('review_id_3', NOW(), NOW(), 'place_id_3', 'user_id_1', 'The location was very good and convenient.'),
        ('review_id_4', NOW(), NOW(), 'place_id_4', 'user_id_1', 'I was satisfied with the food, the view, and the service in general, all 5 stars without question.');

-- Amenities テーブルにデータを追加
INSERT INTO amenities (id, created_at, updated_at, name) 
VALUES ('amenity_id_1', NOW(), NOW(), 'WiFi'),
	('amenity_id_2', NOW(), NOW(), 'Spa'),
        ('amenity_id_3', NOW(), NOW(), 'Toothbrush'),
        ('amenity_id_4', NOW(), NOW(), 'bathtub');

