package za.co.entelect.training.musketeers.repository.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import za.co.entelect.training.musketeers.model.Gender;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "musketeer")
public class MusketeerEntity extends AbstractBaseEntity {

    @NotBlank
    @Column(name = "name", nullable = false)
    private String name;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "gender", nullable = false, length = 16)
    private Gender gender;

    @NotBlank
    @Column(name = "title", nullable = false, length = 128)
    private String title;

    @NotBlank
    @Column(name = "nationality", nullable = false, length = 128)
    private String nationality;

    @Column(name = "occupation", nullable = true, length = 128)
    private String occupation;

    @NotNull
    @Column(name = "date_of_birth", nullable = true)
    private LocalDate dateOfBirth;
}
