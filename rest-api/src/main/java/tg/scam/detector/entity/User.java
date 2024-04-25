package tg.scam.detector.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import tg.scam.detector.entity.converter.EnumRoleUserConverter;

import java.util.Arrays;
import java.util.UUID;

@Data
@Entity
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "users")
public class User {
    @Id
    @Column(name = "user_id")
    private UUID id = UUID.randomUUID();
    @Convert(converter = EnumRoleUserConverter.class)
    private Role role;
    private long tgId;
    private String screenName;
    private String numberPhone;
    private String gamenick;

    public User(Role role, long tgId, String screenName, String numberPhone) {
        this.role = role;
        this.tgId = tgId;
        this.screenName = screenName;
        this.numberPhone = numberPhone;
    }

    @Getter
    public enum Role {
        USER(1), ADMIN(2), MASTER(3);

        private final int id;

        Role(int id) {
            this.id = id;
        }

        public static Role search(int id) {
            return Arrays.stream(Role.values()).filter(role -> role.getId() == id).findFirst().orElseThrow();
        }
    }
}

