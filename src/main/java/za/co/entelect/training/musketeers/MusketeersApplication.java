package za.co.entelect.training.musketeers;

import org.jeasy.random.EasyRandom;
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

@SpringBootApplication
public class MusketeersApplication implements ApplicationRunner {

    public static final int CAPACITY = 100;
    @Autowired
    private MusketeerRepository repository;

    public static void main(String[] args) {
        SpringApplication.run(MusketeersApplication.class, args);
    }

    @Override
    public void run(final ApplicationArguments args) throws Exception {

        final EasyRandom easyRandom = new EasyRandom();

        final List<MusketeerEntity> entities = new ArrayList<>(CAPACITY);

        for (int i = 0; i < CAPACITY; i++) {
            entities.add(
                MusketeerEntity.builder()
                               .name(
                                   easyRandom.nextObject(String.class)
                               )
                               .gender(
//                                   Gender.values()[random.nextInt(Gender.values().length)]
                                   easyRandom.nextObject(Gender.class)
                               )
                               .title(
                                   easyRandom.nextObject(String.class)
                               )
                               .nationality(
                                   easyRandom.nextObject(String.class)
                               )
                               .occupation(
                                   easyRandom.nextObject(String.class)
                               )
                               .dateOfBirth(
//                                   LocalDate.ofEpochDay(random.nextLong(LocalDate.now().toEpochDay()))
                                   easyRandom.nextObject(LocalDate.class)
                               )
                               .build()
            );
        }

        this.repository.saveAll(entities);
    }
}
