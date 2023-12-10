package com.testautomation;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.web.WebApplicationInitializer;

@SpringBootApplication(scanBasePackages = "com.testautomation")
public class Application extends SpringBootServletInitializer implements WebApplicationInitializer {
    private static final Class<Application> MAIN_CLASS = Application.class;

    public static void main(String[] args) {
        SpringApplication.run(MAIN_CLASS, args);
    }

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(MAIN_CLASS);
    }

}
