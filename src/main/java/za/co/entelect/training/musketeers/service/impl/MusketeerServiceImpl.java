package za.co.entelect.training.musketeers.service.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.publisher.MonoSink;
import za.co.entelect.training.musketeers.mapper.MusketeerEntityMapper;
import za.co.entelect.training.musketeers.model.Musketeer;
import za.co.entelect.training.musketeers.repository.MusketeerRepository;
import za.co.entelect.training.musketeers.repository.entity.MusketeerEntity;
import za.co.entelect.training.musketeers.service.MusketeerService;

import javax.persistence.EntityNotFoundException;

@Service
@RequiredArgsConstructor
public class MusketeerServiceImpl implements MusketeerService {

    private final MusketeerRepository repository;
    private final MusketeerEntityMapper mapper;

    @Override
    public Mono<Musketeer> create(final Musketeer musketeer) {
        return Mono.just(musketeer)
            .map((Musketeer domain) -> {
                return mapper.map(domain);
            })
            .map((MusketeerEntity entity) -> {
                return repository.save(entity);
            })
            .map((MusketeerEntity entity) -> {
                return mapper.map(entity);
            });
    }

    @Override
    public Mono<Musketeer> get(final Long id) {
        return Mono.just(
            repository
                .findById(id)
                .map(mapper::map)
                .orElseThrow(EntityNotFoundException::new)
        );
    }

    @Override
    public Mono<Musketeer> update(final Long id, final Musketeer musketeer) {
        return Mono.just(
                repository
                    .findById(id)
                    .map((MusketeerEntity entity) -> {
                        return mapper.map(entity);
                    })
                    .orElseThrow(EntityNotFoundException::new)
            )
            .map((Musketeer that) -> {
                return that.copy(musketeer);
            })
            .map(mapper::map)
            .map(repository::save)
            .map(mapper::map);
    }

    @Override
    public Mono<Void> delete(final Long id) {
        return Mono.create((MonoSink<Void> monoSink) -> {
            repository.deleteById(id);
            monoSink.success();
        });
    }

    @Override
    public Flux<Musketeer> get() {
        final Iterable<MusketeerEntity> all = repository.findAll();
        return Flux.fromIterable(
            all
        ).map(mapper::map);
    }
}
