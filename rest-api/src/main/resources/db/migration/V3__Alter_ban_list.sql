ALTER TABLE ban_list ADD COLUMN owner_id UUID;

ALTER TABLE ban_list ADD CONSTRAINT owner_id_fkey FOREIGN KEY (owner_id) REFERENCES users (user_id);