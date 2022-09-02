package za.co.entelect.training.musketeers.controller.resource;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;

public class MusketeerResource {

    private Long id;

    @NotEmpty
    private String name;

    @NotNull
    private LocalDate dateOfBirth;

    @NotEmpty
    private String placeOfBirth;
}
