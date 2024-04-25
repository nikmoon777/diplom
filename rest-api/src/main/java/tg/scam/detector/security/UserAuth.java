package tg.scam.detector.security;

import org.springframework.security.core.authority.SimpleGrantedAuthority;

import java.util.List;

public record UserAuth(long tgId, List<SimpleGrantedAuthority> authorities) {
}
