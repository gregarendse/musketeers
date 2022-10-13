package za.co.entelect.training.musketeers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import za.co.entelect.training.musketeers.model.Gender;
import za.co.entelect.training.musketeers.repository.MusketeerRepository;
import za.co.entelect.training.musketeers.repository.entity.MusketeerEntity;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@SpringBootApplication
public class MusketeersApplication implements ApplicationRunner {

    public static final int CAPACITY = 100;
    public static final Random RANDOM = new Random();
    @Autowired
    private MusketeerRepository repository;

    public static void main(String[] args) {
        SpringApplication.run(MusketeersApplication.class, args);
    }

    public static String randomString(final int length) {
        int leftLimit = 48; // numeral '0'
        int rightLimit = 122; // letter 'z'

        return RANDOM.ints(leftLimit, rightLimit + 1)
                     .filter(i -> (i <= 57 || i >= 65) && (i <= 90 || i >= 97))
                     .limit(length)
                     .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
                     .toString();
    }

    public static LocalDate randomLocalDate() {
        return LocalDate.ofEpochDay(RANDOM.nextLong(LocalDate.now().toEpochDay()));
    }

    public static Gender randomGender() {
        return Gender.values()[RANDOM.nextInt(Gender.values().length)];
    }

    @Override
    public void run(final ApplicationArguments args) throws Exception {

        final List<MusketeerEntity> entities = new ArrayList<>(CAPACITY);

        for (int i = 0; i < CAPACITY; i++) {
            entities.add(
                MusketeerEntity.builder()
                               .name(
                                   randomString(10)
                               )
                               .gender(
                                   randomGender()
                               )
                               .title(
                                   randomString(3)
                               )
                               .nationality(
                                   randomString(10)
                               )
                               .occupation(
                                   randomString(10)
                               )
                               .dateOfBirth(
                                   randomLocalDate()
                               )
                               .build()
            );
        }

        this.repository.saveAll(entities);
    }
}
