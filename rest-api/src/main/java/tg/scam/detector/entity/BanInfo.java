package tg.scam.detector.entity;

import com.fasterxml.jackson.databind.JsonNode;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import org.springframework.data.rest.core.annotation.RestResource;

import java.util.UUID;

@Data
@Entity
@NoArgsConstructor
@Table(name = "ban_list")
public class BanInfo {
    @Id
    @Column(name = "ban_id")
    private UUID id = UUID.randomUUID();
    @OneToOne
    @JoinColumn(name = "user_id")
    @RestResource(exported = false)
    private User user;
    private String cause;
    @JdbcTypeCode(SqlTypes.JSON)
    private JsonNode proofs;
    @ManyToOne
    @JoinColumn(name="owner_id")
    @RestResource(exported = false)
    private User owner;

    public BanInfo(User user, String cause) {
        this.user = user;
        this.cause = cause;
    }
}
