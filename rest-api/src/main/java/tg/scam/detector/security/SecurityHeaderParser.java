package tg.scam.detector.security;

import lombok.Getter;

import java.util.function.Consumer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Getter
public class SecurityHeaderParser {
    private static final Pattern PATTERN_VALUE = Pattern.compile("(\\w+)\\[(\\w+)]");

    private final String header, secretKey, secretValue, realSecretKey;

    public SecurityHeaderParser(String header, String realKey) {
        this.header = header;
        this.realSecretKey = realKey;

        Matcher matcher = PATTERN_VALUE.matcher(header);
        if (realKey.matches("\\w+") && matcher.find()) {
            this.secretKey = matcher.group(1);
            this.secretValue = matcher.group(2);
        } else {
            throw new RuntimeException("Find incorrect pattern header value");
        }
    }

    public static SecurityHeaderParser parse(String header, String realKey) {
        return new SecurityHeaderParser(header, realKey);
    }

    public boolean isValidKey() {
        return realSecretKey.equals(secretKey);
    }

    public void ifKeyValid(Consumer<String> consumer) {
        if (this.isValidKey()) {
            consumer.accept(secretValue);
        }
    }
}
