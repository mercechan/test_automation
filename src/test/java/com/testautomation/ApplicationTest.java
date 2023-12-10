package com.testautomation;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@Slf4j
@SpringBootTest(classes = Application.class)
@ActiveProfiles("local")
public class ApplicationTest {
    @Test
    void contextLoads() {
    }

}
