package za.co.entelect.training.musketeers.controller.resource;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import za.co.entelect.training.musketeers.model.Gender;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MusketeerResource {

    private Long id;

    @NotBlank
    private String name;

    @NotNull
    private Gender gender;

    @NotBlank
    private String title;

    @NotBlank
    private String nationality;

    private String occupation;

    @NotNull
    private LocalDate dateOfBirth;
}
