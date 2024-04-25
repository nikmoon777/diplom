package tg.scam.detector.repository;

import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.data.rest.core.annotation.RestResource;
import tg.scam.detector.entity.BanInfo;

import java.util.UUID;

@Tag(name = "BanController")
@RepositoryRestResource(path = "ban", itemResourceRel = "ban")
public interface BanInfoRepository extends JpaRepository<BanInfo, UUID> {
    @RestResource(path = "existsByUser", rel = "existsByUser")
    boolean existsByUser_TgId(long tgId);
    @RestResource(path = "byTgId", rel = "byTgId")
    BanInfo findByUser_TgId(long tgId);
}
