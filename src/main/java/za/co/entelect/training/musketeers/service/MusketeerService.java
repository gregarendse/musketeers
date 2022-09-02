package za.co.entelect.training.musketeers.service;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import za.co.entelect.training.musketeers.model.Musketeer;

public interface MusketeerService {
    Mono<Musketeer> create(Musketeer musketeer);

    Mono<Musketeer> get(Long id);

    Mono<Musketeer> update(Long id);

    Mono<Void> delete(Long id);

    Flux<Musketeer> get();
}
