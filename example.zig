const std = @import("std");
const nn = @import("nn.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer _ = gpa.deinit();

    // architecture: 2 -> 2 -> 1
    const arch = [_]usize{ 2, 2, 1 };

    var neural = try nn.NN.nn_alloc(allocator, &arch);
    var gradient = try nn.NN.nn_alloc(allocator, &arch);
    defer neural.deinit(allocator);
    defer gradient.deinit(allocator);

    var td = [_]f32{
        0, 0, 0,
        0, 1, 0,
        1, 0, 0,
        1, 1, 1,
    };

    const training_input = nn.Matrix{
        .rows = 4,
        .cols = 2,
        .data = td[0..],
        .stride = 3,
    };

    const training_output = nn.Matrix{
        .rows = 4,
        .cols = 1,
        .data = td[2..],
        .stride = 3,
    };

    try neural.nn_rand(-1, 1);

    // Just stir up the pile
    const epochs = 10000;
    const rate = 1;
    const eps = 1e-4;

    std.debug.print("\nTraining XOR gate...\n", .{});
    for (0..epochs) |i| {
        nn.NN.nn_finite_diff(neural, gradient, eps, training_input, training_output);

        nn.NN.nn_learn(neural, gradient, rate);

        if (i % 1000 == 0) {
            const cost = nn.NN.neural_cost(neural, training_input, training_output);
            std.debug.print("Epoch {d}: cost = {d:.6}\n", .{ i, cost });
        }
    }

    std.debug.print("\nTesting XOR gate:\n", .{});
    for (0..4) |i| {
        const x = training_input.mat_row(i);
        neural.as[0].mat_copy(x);
        nn.NN.nn_forward(neural);

        std.debug.print("Input: ({d:.0}, {d:.0}) -> Output: {d:.6}\n", .{
            training_input.mat_at(i, 0).*,
            training_input.mat_at(i, 1).*,
            neural.as[neural.count].mat_at(0, 0).*,
        });
    }
}
