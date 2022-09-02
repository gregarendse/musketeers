package za.co.entelect.training.musketeers.respository.entity;

import lombok.Data;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import java.time.LocalDate;

@Data
@Entity
@Table(name = "musketeer")
public class MusketeerEntity extends AbstractBaseEntity {

    @Column(name = "name")
    private String name;

//    private Set<String> aliases;

    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;

    @Column(name = "place_of_birth")
    private String placeOfBirth;
}
