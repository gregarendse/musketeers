package za.co.entelect.training.musketeers.mapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;
import za.co.entelect.training.musketeers.model.Musketeer;
import za.co.entelect.training.musketeers.repository.entity.MusketeerEntity;

@Mapper(
        injectionStrategy = InjectionStrategy.CONSTRUCTOR,
        componentModel = MappingConstants.ComponentModel.SPRING
)
public interface MusketeerEntityMapper {

    MusketeerEntity map(final Musketeer domain);

    Musketeer map(final MusketeerEntity entity);
}
