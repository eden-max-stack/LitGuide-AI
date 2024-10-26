// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  messages: defineTable({
    author: v.string(),
    message: v.any(),
    type: v.string(),
  }),

  keywords: defineTable({
    keyword: v.string(),
  }),
});

