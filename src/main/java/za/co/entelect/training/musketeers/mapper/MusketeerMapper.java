package za.co.entelect.training.musketeers.mapper;

import org.mapstruct.Mapper;
import za.co.entelect.training.musketeers.controller.resource.MusketeerResource;
import za.co.entelect.training.musketeers.model.Musketeer;

@Mapper
public interface MusketeerMapper {

    Musketeer map(final MusketeerResource resource);

    MusketeerResource map(final Musketeer domain);
}
