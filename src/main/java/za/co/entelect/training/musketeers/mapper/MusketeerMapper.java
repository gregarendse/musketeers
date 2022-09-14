package za.co.entelect.training.musketeers.mapper;

import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;
import za.co.entelect.training.musketeers.controller.resource.MusketeerResource;
import za.co.entelect.training.musketeers.model.Musketeer;

@Mapper(
    injectionStrategy = InjectionStrategy.CONSTRUCTOR,
    componentModel = MappingConstants.ComponentModel.SPRING
)
public interface MusketeerMapper {

    Musketeer map(final MusketeerResource resource);

    MusketeerResource map(final Musketeer domain);
}
