package za.co.entelect.training.musketeers.model;

import lombok.Data;

import java.time.LocalDate;

@Data
public class AbstractBase {
    private Long id;
    private Long lockVersion;
    private LocalDate created;
    private LocalDate updated;
}
