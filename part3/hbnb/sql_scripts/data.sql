-- Admin User
INSERT INTO users (
    id, first_name, last_name, email, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$3XfFiWj7LOd0lTST7jYIQ.POQp9MOzZz7i/OqO1ZyG3NnN1OZt69y',  -- hashed "admin1234"
    TRUE
);

-- Insert Amenities with random UUIDs
INSERT INTO amenities (id, name) VALUES
('b362e49a-b981-41b7-90e7-b9f321934312', 'WiFi'),
('cd1035d5-5b7e-4e38-802a-7d918d75b9d2', 'Swimming Pool'),
('eecb58d0-4da7-41a1-9fc3-633fcb10f0c6', 'Air Conditioning');
