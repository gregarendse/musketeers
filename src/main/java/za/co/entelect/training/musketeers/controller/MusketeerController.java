package za.co.entelect.training.musketeers.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import za.co.entelect.training.musketeers.controller.resource.MusketeerResource;
import za.co.entelect.training.musketeers.mapper.MusketeerMapper;
import za.co.entelect.training.musketeers.service.MusketeerService;

import javax.validation.Valid;

@RequiredArgsConstructor
@RestController
public class MusketeerController {

    private final MusketeerService musketeerService;
    private final MusketeerMapper mapper;

    @PostMapping
    public Mono<MusketeerResource> create(
        @RequestBody @Valid final MusketeerResource resource
    ) {
        return this.musketeerService.create(mapper.map(resource)).map(mapper::map);
    }

    @GetMapping("/{id}")
    public Mono<MusketeerResource> get(
        @PathVariable final Long id
    ) {
        return this.musketeerService.get(id).map(mapper::map);
    }

    @PutMapping("/{id}")
    public Mono<MusketeerResource> update(
        @PathVariable final Long id, @RequestBody @Valid final MusketeerResource resource
    ) {
        return this.musketeerService.update(id).map(mapper::map);
    }

    @DeleteMapping("/{id}")
    public Mono<ResponseEntity<Void>> delete(
        @PathVariable final Long id
    ) {
        return this.musketeerService.delete(id).map(unused -> ResponseEntity.ok(null));
    }

    @GetMapping("/")
    public Flux<MusketeerResource> get() {
        return this.musketeerService.get().map(mapper::map);
    }
}
