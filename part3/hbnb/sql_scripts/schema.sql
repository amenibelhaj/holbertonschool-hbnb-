-- Enable foreign key constraints (for SQLite)
PRAGMA foreign_keys = ON;

-- User Table
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,                      -- UUID for the user (CHAR(36))
    first_name VARCHAR(255) NOT NULL,              -- First name of the user (non-nullable)
    last_name VARCHAR(255) NOT NULL,               -- Last name of the user (non-nullable)
    email VARCHAR(255) UNIQUE NOT NULL,            -- Email, must be unique and non-nullable
    password VARCHAR(255) NOT NULL,                -- Password (hashed) (non-nullable)
    is_admin BOOLEAN DEFAULT FALSE                -- Admin flag (default: FALSE)
);

-- Place Table
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,                       -- UUID for the place (CHAR(36))
    title VARCHAR(255) NOT NULL,                   -- Title of the place (non-nullable)
    description TEXT NOT NULL,                     -- Description of the place (non-nullable)
    price DECIMAL(10, 2) NOT NULL,                 -- Price of the place (non-nullable)
    latitude FLOAT NOT NULL,                       -- Latitude (non-nullable)
    longitude FLOAT NOT NULL,                      -- Longitude (non-nullable)
    owner_id CHAR(36),                             -- User ID of the place owner (foreign key)
    FOREIGN KEY (owner_id) REFERENCES users(id)   -- Foreign key reference to the users table
);

-- Review Table
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,                       -- UUID for the review (CHAR(36))
    text TEXT,                                     -- Review text (nullable)
    rating INT CHECK (rating >= 1 AND rating <= 5), -- Rating between 1 and 5
    user_id CHAR(36),                              -- User ID who wrote the review (foreign key)
    place_id CHAR(36),                             -- Place ID being reviewed (foreign key)
    FOREIGN KEY (user_id) REFERENCES users(id),    -- Foreign key reference to the users table
    FOREIGN KEY (place_id) REFERENCES places(id),  -- Foreign key reference to the places table
    UNIQUE (user_id, place_id)                     -- Ensures a user can only leave one review per place
);

-- Amenity Table
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,                      -- UUID for the amenity (CHAR(36))
    name VARCHAR(255) UNIQUE NOT NULL              -- Name of the amenity (must be unique and non-nullable)
);

-- Place_Amenity Join Table (Many-to-Many Relationship between places and amenities)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36),                             -- Place ID (foreign key)
    amenity_id CHAR(36),                           -- Amenity ID (foreign key)
    PRIMARY KEY (place_id, amenity_id),            -- Composite primary key
    FOREIGN KEY (place_id) REFERENCES places(id),  -- Foreign key reference to the places table
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) -- Foreign key reference to the amenities table
);
