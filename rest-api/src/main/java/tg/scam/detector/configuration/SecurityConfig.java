package tg.scam.detector.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import tg.scam.detector.security.AuthProvider;

@Configuration
public class SecurityConfig {
    private final AuthProvider authProvider;

    public SecurityConfig(AuthProvider authProvider) {
        this.authProvider = authProvider;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http.cors(AbstractHttpConfigurer::disable).csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .addFilterBefore(authProvider, UsernamePasswordAuthenticationFilter.class)
                .authorizeHttpRequests(authorize -> {
                    authorize
                            .requestMatchers("/docs", "/swagger-ui/**", "/v3/api-docs/**").permitAll()
                            .requestMatchers(HttpMethod.POST, "/users/*", "/ban/*").hasRole("MASTER")
                            .requestMatchers(HttpMethod.PUT, "/users", "/users/*", "/ban/**").hasRole("MASTER")
                            .requestMatchers(HttpMethod.DELETE, "/users", "/users/*").hasRole("MASTER")
                            .requestMatchers(HttpMethod.PATCH, "/users", "/users/*", "/ban/**").hasRole("MASTER")
                            .requestMatchers(HttpMethod.POST, "/users", "/ban").hasRole("ADMIN")
                            .requestMatchers(HttpMethod.DELETE, "/ban/**").hasRole("ADMIN")
                            .requestMatchers(HttpMethod.GET, "/users/search/by*").hasRole("ADMIN")
                            .requestMatchers(HttpMethod.GET, "/users", "/users/*", "/ban/**").permitAll()
                            .anyRequest().authenticated();
                })
                .build();
    }
}
