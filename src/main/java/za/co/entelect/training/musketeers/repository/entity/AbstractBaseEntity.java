package za.co.entelect.training.musketeers.repository.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import java.time.LocalDateTime;


@Data
@AllArgsConstructor
@NoArgsConstructor
@MappedSuperclass
public abstract class AbstractBaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Version
    @Column(nullable = false, name = "lock_version", columnDefinition = "BIGINT NOT NULL DEFAULT 0")
    private Long lockVersion;

    @CreationTimestamp
    @Column(nullable = false, updatable = false, columnDefinition = "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime created;

    @UpdateTimestamp
    @Column(nullable = false, columnDefinition = "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP")
    private LocalDateTime updated;
}
