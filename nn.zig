const std = @import("std");
const assert = std.debug.assert;
const math = std.math;

pub const Matrix = struct {
    rows: usize,
    cols: usize,
    stride: usize,
    data: []f32,

    pub fn mat_alloc(allocator: std.mem.Allocator, rows: usize, cols: usize) !Matrix {
        return Matrix{
            .rows = rows,
            .cols = cols,
            .stride = cols,
            .data = try allocator.alloc(f32, rows * cols),
        };
    }

    pub fn deinit(self: Matrix, allocator: std.mem.Allocator) void {
        allocator.free(self.data);
    }

    pub fn mat_fill(self: Matrix, x: f32) void {
        for (0..self.rows) |row| {
            for (0..self.cols) |col| {
                self.mat_at(row, col).* = x;
            }
        }
    }

    pub fn mat_rand(self: Matrix, low: f32, high: f32) !void {
        var prng = std.rand.DefaultPrng.init(69);
        const rand = prng.random();

        var a = rand.float(f32) * (high - low) + low;
        for (0..self.rows) |row| {
            for (0..self.cols) |col| {
                self.mat_at(row, col).* = a;
                a = rand.float(f32) * (high - low) + low;
            }
        }
    }

    pub fn mat_sum(self: Matrix, a: Matrix) void {
        assert(a.rows == self.rows);
        assert(a.cols == self.cols);

        for (0..self.rows) |row| {
            for (0..self.cols) |col| {
                self.mat_at(row, col).* += a.mat_at(row, col).*;
            }
        }
    }

    pub fn mat_copy(self: Matrix, src: Matrix) void {
        assert(self.rows == src.rows);
        assert(self.cols == src.cols);

        for (0..self.rows) |row| {
            for (0..self.cols) |col| {
                self.mat_at(row, col).* = src.mat_at(row, col).*;
            }
        }
    }

    pub fn mat_row(self: Matrix, row: usize) Matrix {
        const start_index = row * self.stride;
        return Matrix{
            .rows = 1,
            .cols = self.cols,
            .stride = self.stride,
            .data = self.data[start_index..(start_index + self.cols)],
        };
    }

    pub fn mat_dot(self: Matrix, a: Matrix, b: Matrix) void {
        assert(a.cols == b.rows);
        assert(self.rows == a.rows);
        assert(self.cols == b.cols);

        self.mat_fill(0);
        for (0..self.rows) |row| {
            for (0..self.cols) |col| {
                for (0..b.rows) |b_row| {
                    self.mat_at(row, col).* += a.mat_at(row, b_row).* * b.mat_at(b_row, col).*;
                }
            }
        }
    }

    pub inline fn mat_at(self: Matrix, row: usize, col: usize) *f32 {
        return &self.data[row * self.stride + col];
    }

    pub fn mat_print(self: Matrix, name: []const u8, padding: usize) void {
        std.debug.print("{s} = [\n", .{name});
        for (0..self.rows) |i| {
            for (0..padding) |_| {
                std.debug.print(" ", .{});
            }
            for (0..self.cols) |j| {
                std.debug.print("{d} ", .{self.mat_at(i, j).*});
            }
            std.debug.print("\n", .{});
        }
        std.debug.print("]\n", .{});
    }

    pub fn mat_sig(self: Matrix) void {
        for (0..self.rows) |row| {
            for (0..self.cols) |col| {
                self.mat_at(row, col).* = sigmoidf(self.mat_at(row, col).*);
            }
        }
    }

    pub fn sigmoidf(x: f32) f32 {
        return 1.0 / (1.0 + math.exp(-x));
    }
};

pub const NN = struct {
    count: usize,
    ws: []Matrix,
    bs: []Matrix,
    as: []Matrix,

    pub fn nn_alloc(allocator: std.mem.Allocator, arch: []const usize) !NN {
        const count = arch.len - 1;
        assert(count > 0);

        const ws = try allocator.alloc(Matrix, count);
        errdefer allocator.free(ws);

        const bs = try allocator.alloc(Matrix, count);
        errdefer allocator.free(bs);

        const as = try allocator.alloc(Matrix, count + 1);
        errdefer allocator.free(as);

        as[0] = try Matrix.mat_alloc(allocator, 1, arch[0]);
        errdefer as[0].deinit(allocator);

        for (1..arch.len) |i| {
            ws[i - 1] = try Matrix.mat_alloc(allocator, as[i - 1].cols, arch[i]);
            bs[i - 1] = try Matrix.mat_alloc(allocator, 1, arch[i]);
            as[i] = try Matrix.mat_alloc(allocator, 1, arch[i]);
        }

        return NN{
            .count = count,
            .ws = ws,
            .bs = bs,
            .as = as,
        };
    }

    pub fn deinit(self: NN, allocator: std.mem.Allocator) void {
        for (0..self.count) |i| {
            self.ws[i].deinit(allocator);
            self.bs[i].deinit(allocator);
            self.as[i].deinit(allocator);
        }
        self.as[self.count].deinit(allocator);
        allocator.free(self.ws);
        allocator.free(self.bs);
        allocator.free(self.as);
    }

    pub fn nn_rand(self: NN, low: f32, high: f32) !void {
        for (0..self.count) |i| {
            try self.ws[i].mat_rand(low, high);
            try self.bs[i].mat_rand(low, high);
        }
    }

    pub fn nn_print(self: NN, name: []const u8) void {
        var buf: [256]u8 = undefined;
        std.debug.print("{s} = [\n", .{name});
        for (0..self.count) |i| {
            const ws_name = std.fmt.bufPrint(&buf, "ws{d}", .{i}) catch unreachable;
            self.ws[i].mat_print(ws_name, 4);
            const bs_name = std.fmt.bufPrint(&buf, "bs{d}", .{i}) catch unreachable;
            self.bs[i].mat_print(bs_name, 4);
        }
        std.debug.print("]\n", .{});
    }

    pub fn nn_forward(nn: NN) void {
        for (0..nn.count) |i| {
            nn.as[i + 1].mat_dot(nn.as[i], nn.ws[i]);
            nn.as[i + 1].mat_sum(nn.bs[i]);
            nn.as[i + 1].mat_sig();
        }
    }

    pub fn neural_cost(neural: NN, ti: Matrix, to: Matrix) f32 {
        assert(ti.rows == to.rows);
        assert(to.cols == neural.as[neural.count].cols);

        var c: f32 = 0;

        for (0..ti.rows) |row| {
            const x = ti.mat_row(row);
            const y = to.mat_row(row);

            neural.as[0].mat_copy(x);
            NN.nn_forward(neural);

            for (0..to.cols) |col| {
                const d = neural.as[neural.count].mat_at(0, col).* - y.mat_at(0, col).*;
                c += d * d;
            }
        }

        return c / @as(f32, @floatFromInt(ti.rows));
    }

    pub fn nn_finite_diff(neural: NN, ng: NN, eps: f32, ti: Matrix, to: Matrix) void {
        var saved: f32 = undefined;

        for (0..neural.count) |i| {
            for (0..neural.ws[i].rows) |row| {
                for (0..neural.ws[i].cols) |col| {
                    saved = neural.ws[i].mat_at(row, col).*;
                    neural.ws[i].mat_at(row, col).* = saved + eps;
                    const cost_plus = neural_cost(neural, ti, to);
                    neural.ws[i].mat_at(row, col).* = saved - eps;
                    const cost_minus = neural_cost(neural, ti, to);
                    ng.ws[i].mat_at(row, col).* = (cost_plus - cost_minus) / (2 * eps);
                    neural.ws[i].mat_at(row, col).* = saved;
                }
            }
        }

        for (0..neural.count) |i| {
            for (0..neural.bs[i].rows) |row| {
                for (0..neural.bs[i].cols) |col| {
                    saved = neural.bs[i].mat_at(row, col).*;
                    neural.bs[i].mat_at(row, col).* = saved + eps;
                    const cost_plus = neural_cost(neural, ti, to);
                    neural.bs[i].mat_at(row, col).* = saved - eps;
                    const cost_minus = neural_cost(neural, ti, to);
                    ng.bs[i].mat_at(row, col).* = (cost_plus - cost_minus) / (2 * eps);
                    neural.bs[i].mat_at(row, col).* = saved;
                }
            }
        }
    }

    pub fn nn_zero(neural: NN) void {
        for (0..neural.count) |i| {
            neural.ws[i].mat_fill(0);
            neural.bs[i].mat_fill(0);
            neural.as[i].mat_fill(0);
        }
        neural.as[neural.count].mat_fill(0);
    }

    pub fn nn_learn(neural: NN, ng: NN, rate: f32) void {
        for (0..neural.count) |i| {
            for (0..neural.ws[i].rows) |row| {
                for (0..neural.ws[i].cols) |col| {
                    neural.ws[i].mat_at(row, col).* -= rate * ng.ws[i].mat_at(row, col).*;
                }
            }

            for (0..neural.bs[i].rows) |row| {
                for (0..neural.bs[i].cols) |col| {
                    neural.bs[i].mat_at(row, col).* -= rate * ng.bs[i].mat_at(row, col).*;
                }
            }
        }
    }
};
