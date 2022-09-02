package za.co.entelect.training.musketeers.service.impl;

import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import za.co.entelect.training.musketeers.model.Musketeer;
import za.co.entelect.training.musketeers.service.MusketeerService;

@Service
public class MusketeerServiceImpl implements MusketeerService {

    @Override
    public Mono<Musketeer> create(final Musketeer musketeer) {
        return Mono.just(musketeer);
    }

    @Override
    public Mono<Musketeer> get(final Long id) {
        return Mono.just(new Musketeer());
    }

    @Override
    public Mono<Musketeer> update(final Long id) {
        return Mono.just(new Musketeer());
    }

    @Override
    public Mono<Void> delete(final Long id) {
        return Mono.empty();
    }

    @Override
    public Flux<Musketeer> get() {
        return Flux.empty();
    }
}
