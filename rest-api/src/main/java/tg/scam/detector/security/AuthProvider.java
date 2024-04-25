package tg.scam.detector.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import tg.scam.detector.entity.User;
import tg.scam.detector.repository.UserRepository;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Component
public class AuthProvider extends OncePerRequestFilter {
    @Value("${service.http.header.name}")
    private String headerName;
    @Getter
    @Value("${service.http.header.secret.key}")
    private String secretKey;
    private final UserRepository userRepository;

    public AuthProvider(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String header = request.getHeader(headerName);
        if (header != null) {
            SecurityHeaderParser.parse(header, secretKey)
                    .ifKeyValid(value -> {
                        long tgId = Long.parseLong(value);
                        userRepository.findByTgId(tgId)
                                .ifPresent(user -> {
                                    List<SimpleGrantedAuthority> authorities = new ArrayList<>();
                                    for (User.Role role : User.Role.values()) {
                                        authorities.add(new SimpleGrantedAuthority("ROLE_" + role.name()));
                                        if (role == user.getRole()) break;
                                    }

                                    UserAuth userAuth = new UserAuth(tgId, authorities);
                                    auth(userAuth, null, authorities);
                                });
                    });
        }

        filterChain.doFilter(request, response);
    }

    private void auth(Object userObject, Object password, List<SimpleGrantedAuthority> authorities) {
        Authentication authentication = new UsernamePasswordAuthenticationToken(userObject, password, authorities);
        SecurityContextHolder.getContext().setAuthentication(authentication);
    }
}
