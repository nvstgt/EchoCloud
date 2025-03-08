import os
import sqlite3

DATABASE = os.path.join(os.getcwd(), "vulnerable.db")

def get_db():
    """Return a new database connection with row_factory set to sqlite3.Row."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initializes the database with required tables and sample data."""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            info TEXT
        )
    ''')
    cursor.execute("INSERT INTO data (info) VALUES ('Sample data entry 1')")
    cursor.execute("INSERT INTO data (info) VALUES ('Another sample info entry')")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            bio TEXT,
            genre TEXT,
            keywords TEXT
        )
    ''')
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('DJ Coolcat', 'Smooth operator of chill vibes with a laid-back style.', 'Lo-fi', 'chill, lo-fi, beats, relaxed')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('SynthMaster', 'Innovative synthesizer wizard blending retro and futuristic sounds.', 'Retro-wave', 'synth, retro, future, beats')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Moonlit', 'Creator of atmospheric, immersive tracks', 'Ambient', 'atmospheric, ambient, immersive')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Diffusse', 'Innovative sound architect, mixing abstract electronic textures.', 'Electronic', 'electronic, abstract, textures')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Electric Dream Machine', 'Revives classic dreams with electrifying performances.', '80s Glam', '80s, glam, electrifying')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Reverse-Flipside', 'Bold, experimental mix master pushing boundaries in electronic music.', 'Experimental', 'experimental, electronic, innovative')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('The Remisses', 'Melodic powerhouse crafting raw, emotive rock anthems.', 'Rock', 'rock, raw, emotive')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Redemption', 'High-energy metal band channeling rebellion and passion.', 'Metal', 'metal, high-energy, rebellion')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Kokikola Pepsico', 'Vibrant pop icon known for infectious hooks and dynamic beats.', 'Pop', 'pop, catchy, vibrant')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Pink Bizmuth', 'Striking metal innovator blending powerful riffs with artistic flair.', 'Metal', 'metal, riffs, innovative')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('But It''s Not A Butt', 'Quirky rock ensemble known for tongue-in-cheek humor and sharp sound.', 'Rock', 'rock, quirky, humorous')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('12-Steps', 'Intense metal outfit exploring themes of struggle and redemption.', 'Metal', 'metal, intense, struggle')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Pulse Width', 'Smooth electronica with rhythmic precision and creative soundscapes.', 'Electronica', 'electronica, smooth, rhythmic')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Groan Putnam', 'Indie pop band with a playful edge and heartfelt melodies.', 'Indie Pop', 'indie, pop, playful')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('A.I. ft. Jeninena Rockham', 'Cutting-edge pop duo merging digital beats with soulful vocals.', 'Pop', 'pop, digital, soulful')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Patty Cam', 'Dance-pop sensation delivering electrifying performances and catchy tunes.', 'Dance-pop', 'dance, pop, electrifying')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('The Bowling Pwns', 'Rock meets bowling alley grunge. Strike after strike of sonic perfection.', 'Rock', 'rock, grunge, perfection')")
    cursor.execute("INSERT INTO artists (name, bio, genre, keywords) VALUES ('Intentionally Bad', 'Metal group embracing chaotic, raw energy to stick it out in the toughest jams.', 'Metal', 'metal, chaotic, raw')")
     
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            favorite_genre TEXT,
            member_since TEXT
        )
    ''')
    
    users = [
        ('TheProfezzorJ', 'Password1!', 'cjohnson@uwsp.edu', 'Tamagochibananarama', '2018'),
        ('Alice', '123456', 'soundwave77@verizon.net', 'Pop', '2020'),
        ('Bob', 'baseball', 'beatfactory@live.com', 'Rock', '2019'),
        ('Charlie', 'iloveyou', 'rhythm_x@protonmail.com', 'Jazz', '2019'),
        ('Dave', 'welcome', 'electrobeatz@outlook.com', 'Hip-Hop', '2018'),
        ('Eve', 'master', 'sonicpulse99@yahoo.com', 'Electronic', '2019'),
        ('Frank', 'sunshine', 'groove_machine@icloud.com', 'Country', '2021'),
        ('Grace', 'trustno1', 'tempo_tide@aol.com', 'Classical', '2020'),
        ('Heidi', '111111', 'tempo_tide@aol.com', 'Reggae', '2022'),
        ('Ivan', 'ivan123', 'basslineblitz@comcast.net', 'Metal', '2020'),
        ('Judy', 'dragon', 'trebletonic@mail.com', 'Blues', '2018'),
        ('Mallory', 'letmein', 'echodreams@zoho.com', 'R&B', '2022'),
        ('Niaj', 'monkey', 'pulse_rider@ymail.com', 'Folk', '2023'),
        ('Olivia', 'abc123', 'rhythmrealm@bellsouth.net', 'Indie', '2023'),
        ('Peggy', 'qwerty', 'audiophantom@gmail.com', 'Alternative', '2023'),
        ('Trent', 'Hunter2', 'basscollective@outlook.com', 'EDM', '2018')
    ]
    
    for username, password, email, favorite_genre, member_since in users:
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, favorite_genre, member_since) VALUES (?, ?, ?, ?, ?)",
                (username, password, email, favorite_genre, member_since)
            )
        except sqlite3.IntegrityError:
            pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            title TEXT,
            artist TEXT
        )
    ''')
    
    uploads = [
        ('Alice', '2024/12/08', 'Stars Align', 'The Bowling Pins'),
        ('Alice', '2024/12/08', 'Electric Hits', 'Patty Cam'),
        ('Charlie', '2024/12/08', 'Floppy Sticks', 'Groan Putnam'),
        ('Dave', '2024/12/08', 'Semt Hard', 'A.I. (Another Idiot) ft. Jeninena Rockham'),
        ('Eve', '2024/12/08', 'Mostly Drunk', '12-Steps'),
        ('Frank', '2024/12/08', 'Midnight Air', 'Pulse Width'),
        ('Grace', '2024/12/08', 'This Looks Like A Butt', 'But Its Not a Butt'),
        ('Mallory', '2024/12/08', 'Digital Bloom', 'Reverse-Flipside'),
        ('Niaj', '2024/12/08', 'Solar Flare', 'Kokikola Pepsico'),
        ('Olivia', '2024/12/08', 'Conducción Nocturna (Night Drive)', 'Moonlit'),
        ('Trent', '2024/12/08', 'Retro Sunset', 'SynthMaster'),
        ('Trent', '2024/12/08', 'The Nightman Cometh', 'Electric Dream Machine'),
        ('Ivan', '2024/12/08', 'Metal Outlaws', 'Redemption'),
        ('Olivia', '2024/12/10', 'Echo Drift', 'Diffusse'),
        ('Peggy', '2024/12/12', 'Chill Vibes 2', 'DJ Coolcat'),
        ('TheProfezzorJ', '2024/12/22', 'Dreadfully Pale', 'The Remisses'),
        ('Heidi', '2024/12/22', 'Lost in Echos', 'Doot-n-Toot'),
        ('Ivan', '2024/12/25', 'Static Shock', 'Pink Bizmuth'),
        ('TheProfezzorJ', '2024/12/25', 'SSTI', 'Pointer Overflow and the CTFs'),
        ('TheProfezzorJ', '2025/01/05', 'Chill Vibes', 'DJ Coolcat'),
        ('Judy', '2025/01/05', 'Stick It Out', 'Intentionally Bad')
    ]
    
    for username, date, title, artist in uploads:
        try:
            cursor.execute(
                "INSERT INTO uploads (username, date, title, artist) VALUES (?, ?, ?, ?)",
                (username, date, title, artist)
            )
        except sqlite3.IntegrityError:
            pass

    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
