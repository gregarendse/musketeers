package za.co.entelect.training.musketeers.model;

import lombok.Data;

import java.time.LocalDate;

@Data
public class Musketeer extends AbstractBase {
    private String name;
    //    private Set<String> aliases;
    private LocalDate dateOfBirth;
    private String placeOfBirth;
}
