package tg.scam.detector.repository;

import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.data.rest.core.annotation.RestResource;
import tg.scam.detector.entity.User;

import java.util.Optional;
import java.util.UUID;

@Tag(name = "UserController")
@RepositoryRestResource(path = "users", itemResourceRel = "users")
public interface UserRepository extends JpaRepository<User, UUID> {
    @RestResource(path = "byName", rel = "byName")
    Optional<User> findByScreenName(String screenName);
    @RestResource(path = "byPhone", rel = "byPhone")
    Optional<User> findByNumberPhone(String numberPhone);
    @RestResource(path = "byTg", rel = "byTg")
    Optional<User> findByTgId(long tgId);
}
