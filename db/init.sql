CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL
);


--DROP TABLE IF EXISTS skins; 
CREATE TABLE IF NOT EXISTS skins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skin_dir TEXT NOT NULL
);


--DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_skin INTEGER,
    FOREIGN KEY (id_skin) REFERENCES skins(id)
);


/*
INSERT INTO skins(skin_dir) 
VALUES 
("GameTextures/TextureSkin1.png"),
("GameTextures/TextureSkin2.png");

INSERT INTO user(id_skin) VALUES (1);
*/