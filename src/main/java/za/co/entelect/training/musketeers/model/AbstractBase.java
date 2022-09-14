package za.co.entelect.training.musketeers.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AbstractBase {
    private Long id;
    private Long lockVersion;
    private LocalDateTime created;
    private LocalDateTime updated;
}
