package za.co.entelect.training.musketeers.repository;

import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;
import za.co.entelect.training.musketeers.repository.entity.MusketeerEntity;

@Repository
public interface MusketeerRepository extends PagingAndSortingRepository<MusketeerEntity, Long> {
}
