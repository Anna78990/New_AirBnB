USE hbnb_dev_db;

INSERT INTO cities (id, created_at, updated_at, name, state_id)
VALUES ('city_id_3', NOW(), NOW(), 'New York', 'state_id_2');

INSERT INTO places (id, created_at, updated_at, city_id, user_id, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude, image) 
VALUES ('place_id_4, NOW(), NOW(), 'city_id_3', 'user_id_1', 'New York Hotel Regency', 
'A hotel offering the highest level of luxury with a 3-star restaurant, bar, and exclus
ive spa', 2, 2, 2, 1000, 37.7749, -122.4194, 'image_url');

INSERT INTO reviews (id, created_at, updated_at, place_id, user_id, text)
VALUES ('review_id_4', NOW(), NOW(), 'place_id_4', 'user_id_1', 'I was satisfied with  
the food, the view, and the service in general, all 5 stars without question.');
