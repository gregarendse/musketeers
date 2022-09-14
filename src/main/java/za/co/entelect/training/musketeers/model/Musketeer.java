package za.co.entelect.training.musketeers.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Musketeer extends AbstractBase {

    private String name;
    private Gender gender;
    private String title;
    private String nationality;
    private String occupation;
    private LocalDate dateOfBirth;

    public Musketeer copy(final Musketeer that) {
        this.name = that.getName();
        this.gender = that.getGender();
        this.title = that.getTitle();
        this.nationality = that.getNationality();
        this.occupation = that.getOccupation();
        this.dateOfBirth = that.getDateOfBirth();
        return this;
    }
}
