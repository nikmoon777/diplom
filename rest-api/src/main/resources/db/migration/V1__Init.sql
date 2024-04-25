CREATE TABLE IF NOT EXISTS user_role (
    role_id INT UNIQUE NOT NULL,
    title VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO user_role (role_id, title)
VALUES (1, 'USER'),
       (2, 'ADMIN'),
       (3, 'MASTER');

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    role INT NOT NULL,
    tg_id BIGINT UNIQUE NOT NULL,
    screen_name VARCHAR(255) UNIQUE,
    number_phone VARCHAR(100) UNIQUE,
    FOREIGN KEY (role) REFERENCES user_role (role_id)
);

INSERT INTO users (user_id, role, tg_id, screen_name, number_phone) 
VALUES ('4f58b895-ecca-497a-b541-b3b14f4e7dff', 3, 834778613, 'nikmayson', '+79539504236');

CREATE TABLE IF NOT EXISTS ban_list (
    ban_id UUID PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL,
    cause TEXT,
    proofs JSON,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);