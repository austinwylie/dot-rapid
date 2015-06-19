CREATE TYPE permission AS ENUM ('owner', 'read', 'write', 'delete');
CREATE TYPE layer_type AS ENUM ('seismic', 'atmospheric', 'demographic');
CREATE TYPE format AS ENUM ('json', 'xml');

CREATE TABLE regions (
    id serial PRIMARY KEY,
    descriptor varchar(256),
    properties text,
    properties_format format,
    geom geometry(polygon, 4326)
);

CREATE TABLE layers (
    id serial PRIMARY KEY,
    region_id int NOT NULL,
    descriptor varchar(256),
    properties text,
    properties_format format,
    geom geometry,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

CREATE TABLE features (
    id serial PRIMARY KEY,
    layer_id int,
    descriptor varchar(256),
    properties text,
    properties_format format,
    geom geometry,
    FOREIGN KEY (feature_series_id) REFERENCES feature_series(id),
    CHECK (st_ndims(geom) = 2), -- Enforces 2 dimensions
    CHECK (st_srid(geom) = 4326) -- Enforces valid lat/long values
);

CREATE TABLE feature_valid_times (
    id serial PRIMARY KEY,
    feature_id int NOT NULL,
    start timestamp,
    stop timestamp,
    FOREIGN KEY (feature_id) REFERENCES features(id)
);

CREATE TABLE external_users (
    id serial PRIMARY KEY,
    descriptor varchar(256)
);

CREATE TABLE api_tokens (
    id serial PRIMARY KEY,
    external_user_id int NOT NULL,
    token text,
    FOREIGN KEY (external_user_id) REFERENCES external_users(id)
);

CREATE TABLE logins (
    id serial PRIMARY KEY,
    external_user_id int NOT NULL,
    password_hash char(20),
    password_salt int,
    FOREIGN KEY (external_user_id) REFERENCES external_users(id)
);

CREATE TABLE layer_active_permissions (
    id serial PRIMARY KEY,
    external_user_id int NOT NULL,
    layer_id int NOT NULL,
    active_permission permission NOT NULL,
    FOREIGN KEY (external_user_id) REFERENCES external_users(id),
    FOREIGN KEY (layer_id) REFERENCES layers(id)
);

CREATE TABLE region_active_permissions (
    id serial PRIMARY KEY,
    external_user_id int NOT NULL,
    region_id int NOT NULL,
    active_permission permission NOT NULL,
    FOREIGN KEY (external_user_id) REFERENCES external_users(id),
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

