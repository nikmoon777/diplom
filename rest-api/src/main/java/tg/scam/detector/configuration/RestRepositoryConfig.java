package tg.scam.detector.configuration;

import jakarta.persistence.EntityManager;
import jakarta.persistence.metamodel.Type;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
import org.springframework.web.servlet.config.annotation.CorsRegistry;

@Configuration
public class RestRepositoryConfig implements RepositoryRestConfigurer {
    private final EntityManager entityManager;

    public RestRepositoryConfig(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Override
    public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config, CorsRegistry cors) {
        entityManager.getMetamodel().getEntities().stream().map(Type::getJavaType).forEach(config::exposeIdsFor);
        RepositoryRestConfigurer.super.configureRepositoryRestConfiguration(config, cors);
    }
}
