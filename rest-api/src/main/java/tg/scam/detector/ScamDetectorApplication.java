package tg.scam.detector;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.PropertySource;

@PropertySource("/service.properties")
@SpringBootApplication
public class ScamDetectorApplication {
	public static void main(String[] args) {
		SpringApplication.run(ScamDetectorApplication.class, args);
	}
}
